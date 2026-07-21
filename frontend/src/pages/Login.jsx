import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import toast from "react-hot-toast";
import "../styles/Auth.css";
const API ="https://rag-chatbot-waz7.onrender.com";
function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        async function checkUser(){
            const token= localStorage.getItem("token");
            if(!token) return;
            try{
                await axios.get(`${API}/me`, 
                    {
                        headers: {
                            Authorization : `Bearer ${token}`
                        }
                    }
                );
                navigate("/chat");
            }
            catch{
                localStorage.removeItem("token");
            }
            
        }
        checkUser();
    }, []);

    async function handleLogin() {
        if (!email || !password) {
            toast.error("Plese fill all fields");
            return;
        }
        try {
            const response = await axios.post(`${API}/login`, { email, password });
            
            const token = response.data.access_token;
            localStorage.setItem("token", token);
            toast.success("Login Successful");
            navigate("/chat");
        } catch (error) {
            const errorMsg = error.response?.data?.detail || "Login Failed";
            toast.error("Please Register First");
        }
    }

    return (
        
  <div className="auth-container">
    <div className="auth-card">
      <h2>Welcome Back 👋</h2>
      <p className="subtitle">
        Login to continue chatting with your AI Assistant
      </p>

      <input
        type="email"
        placeholder="Email Address"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        autoCapitalize="off"
      />

      <div className="password-box">

<input
type={showPassword ? "text" : "password"}
placeholder="Password"
value={password}
onChange={(e)=>setPassword(e.target.value)}
autoComplete="new-password"
/>

<button
type="button"
className="eye-btn"
onClick={()=>setShowPassword(!showPassword)}
>

{showPassword ? "🙈" : "👁️"}

</button>

</div>

      <button className="auth-btn"
       onClick={handleLogin}>
        Login
      </button>

      <p className="switch-text">
        Don't have an account?
        <Link to="/register"> Register</Link>
      </p>
    </div>
  </div>
);
    
}

export default Login;