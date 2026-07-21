import {Navigate } from "react-router-dom";
import { useState,useEffect } from "react";
import axios from "axios";
const API ="https://rag-chatbot-waz7.onrender.com";
function ProtectedRoute({children}){
    const[loading,setLoading]=useState(true);
    const [isValid,setIsValid]=useState(false);
    useEffect(() => {
        async function verifyToken(){
            const token= localStorage.getItem("token");
            console.log("LOCAL TOKEN =", token);
            if (!token){
                setLoading(false);
                return;
            }
            try{
                await axios.get(`${API}/me`,
                    {
                        headers:{
                            Authorization: `Bearer ${token}`
                        }
                    }
                );
                setIsValid(true);
            }
            catch{
                localStorage.removeItem("token");
                setIsValid(false);          
             }
             finally{
                setLoading(false);

             }
        }
        
            verifyToken();
        },[]);

        if (loading){
            return <h2>Loading...</h2>
        }
        if (!isValid){
            return <Navigate to ="/"  />

        }
        return children;

    }
export default ProtectedRoute;