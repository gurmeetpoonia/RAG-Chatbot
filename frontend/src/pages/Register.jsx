import { useState ,useEffect} from "react";
import axios from "axios";
import { useNavigate,Link} from "react-router-dom";
import toast from "react-hot-toast";
import "../styles/Auth.css";
const API ="https://rag-chatbot-0ul0.onrender.com";

function Register(){
    const [username,setUsername]= useState("");
    const[email,setEmail]=useState("");
    const [password,setPassword]=useState("");
    const [showPassword,setShowPassword]=useState(false);
    const navigate=useNavigate();

    useEffect(()=> {
        const token =localStorage.getItem("token");
        if (token){
            navigate("/chat");
        }
    } ,[]);
    async function handleRegister() {
        try {
            const response = await axios.post(
                `${API}/register`,
                {
                    username,
                    email,
                    password
                }
            );

            console.log(response.data);
            toast.success("Registration Successful");

            navigate("/");

        } catch (error) {

            console.log("Full Error:", error);

            if (error.response) {
                console.log("Status:", error.response.status);
                console.log("Data:", error.response.data);
            } else if (error.request) {
                console.log("No Response:", error.request);
            } else {
                console.log("Message:", error.message);
            }
        }
    }
            
        
    return (
  <div className="auth-container">

    <div className="auth-card">
      <h2>Create Account 🚀</h2>

      <p className="subtitle">
        Register to start using your AI Chatbot
      </p>

      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      <input
        type="email"
        placeholder="Email Address"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        autoComplete="off"
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
       onClick={handleRegister}>
        Register
      </button>

      <p className="switch-text">
        Already have an account?
        <Link to="/"> Login</Link>
      </p>
    </div>

  </div>
);
}
export default Register;