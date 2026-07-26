import { useEffect, useState, useRef } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import Swal from "sweetalert2";
import Sidebar from "../components/Sidebar";
import { ArrowUp ,Plus} from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "../styles/chat.css";
import "../styles/Sidebar.css";
import "../styles/modal.css";
import "../styles/empty.css";
import { FiTerminal } from "react-icons/fi";
const API ="https://rag-chatbot-n0iw.onrender.com";

function Chat() {
    const [pdfs, setPdfs] = useState([]);
    const [question, setQuestion] = useState("");
    const [isTyping, setIsTyping] = useState(false);
    const [messages, setMessages] = useState([]);
    const [uploading, setUploading] = useState(false);

    const chatEndRef = useRef(null);
    const fileInputRef = useRef(null);
    const [chats, setChats] = useState([]);
    const [selectedConversation, setSelectedConversation] = useState(null);
    const [conversationPDFs, setConversationPDFs] = useState([]);
    const [newChatLoading, setNewChatLoading] = useState(false);
    const [deletingId, setDeletingId] = useState(null);
    const token = localStorage.getItem("token");
    const navigate = useNavigate();
    const [sidebarWidth, setSidebarWidth] = useState(
    Number(localStorage.getItem("sidebarWidth")) || 280
);

    const isResizing = useRef(false);
    useEffect(() => {

    function handleMouseMove(e) {

        if (!isResizing.current) return;

        const newWidth = Math.min(
            Math.max(e.clientX, 220),
            450
        );

        setSidebarWidth(newWidth);
    }

    function handleMouseUp() {

        isResizing.current = false;
        document.body.style.cursor = "default";
        document
            .querySelector(".sidebar")
            ?.classList.remove("resizing");

        localStorage.setItem(
            "sidebarWidth",
            sidebarWidth
        );
    }

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);

    return () => {

        window.removeEventListener("mousemove", handleMouseMove);
        window.removeEventListener("mouseup", handleMouseUp);

    };

}, [sidebarWidth]);
    // ==============================
    // Auth Functions
    // ==============================

    function handleUnauthorized(error) {
        if (error.response?.status === 401) {
            localStorage.removeItem("token");
            navigate("/");
            return true;
        }
        return false;
    }
    function logout() {
        localStorage.removeItem("token");
        navigate("/");
    }
    // ==============================
    // API Functions
    // ==============================

    async function fetchPDFs() {
        try {
            const response = await axios.get(`${API}/my-pdfs`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setPdfs(response.data);
        } catch (error) {
            if (handleUnauthorized(error)) return;
            console.error(error);
        }
    }

    async function fetchChats() {
        try {
            const response = await axios.get(`${API}/history`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setChats(response.data);
        } catch (error) {
            if (handleUnauthorized(error)) return;
            console.error(error);
        }
    }

    useEffect(() => {
        if (!token) {
            navigate("/");
            return;
        }
        fetchPDFs();
        fetchChats();
    }, []);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, isTyping]);

    // ==============================
    // Conversation Functions
    // ==============================
    async function createConversation() {
        
        setNewChatLoading(true);
        try {
            const response = await axios.post(
                `${API}/conversation/create`,
                {},
                {
                    headers: { Authorization: `Bearer ${token}` }
                }
            );

            const newConversation = {
                ...response.data,
                pdfs:[]
            };

            setSelectedConversation(newConversation);

            await fetchChats();

            openConversation(newConversation);
            setMessages([]);
            
            toast.success("New Chat Created");
        } catch (error) {
            if (handleUnauthorized(error)) return;
            toast.error(error.response?.data?.detail || "Unable to create chat");
        } finally{
            setNewChatLoading(false);
        }
    }

    async function openConversation(conversation) {

    setSelectedConversation(conversation);

    setConversationPDFs(conversation.pdfs || []);

    try {

        const response = await axios.get(
            `${API}/conversation/${conversation.id}/messages`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );
        
        const data = [];

        response.data.forEach(chat => {

            data.push({
                role: "user",
                text: chat.question
            });

            data.push({
                role: "ai",
                text: chat.answer
            });

        });

        setMessages(data);

    }
    catch (error) {

        toast.error("Unable to load chat");

    }
}

    async function renameConversation(conversation) {
        const { value } = await Swal.fire({
            title: "Rename Chat",
            input: "text",
            inputValue: conversation.title,
            showCancelButton: true,
            confirmButtonText: "Save"
        });

        if (!value) return;

        try {
            await axios.put(
                `${API}/conversation/${conversation.id}/rename`,
                { title: value },
                {
                    headers: { Authorization: `Bearer ${token}` }
                }
            );
            toast.success("Chat Renamed");
            fetchChats();
        } catch {
            toast.error("Rename Failed");
        }
    }
    async function deleteConversation(id) {
        const result = await Swal.fire({
            title: "Delete Chat?",
            icon: "warning",
            showCancelButton: true,
            confirmButtonText: "Delete"
        });

        if (!result.isConfirmed) return;
        setDeletingId(id);
        try {
            await axios.delete(`${API}/conversation/${id}`, {
                headers: { Authorization: `Bearer ${token}` }
            });

            toast.success("Chat Deleted");
            if (selectedConversation?.id === id) {
                setSelectedConversation(null);
                setMessages([]);
            }
            fetchChats();
        } catch {
            toast.error("Delete Failed");
        }finally{
            setDeletingId(null);
        }
    }
    // ==============================
    // PDF Functions
    // ==============================
    async function handleFileSelect(e) {

    const selectedFile = e.target.files[0];

    if (!selectedFile) return;
    setUploading(true);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {

        let conversation = selectedConversation;

        // Agar koi conversation select nahi hai
        if (!conversation) {

            const res = await axios.post(
                `${API}/conversation/create`,
                {},
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            conversation = {
                ...res.data,
                pdfs: []
            };

            setSelectedConversation(conversation);
        }

        // Upload PDF
        const response = await axios.post(
            `${API}/upload`,
            formData,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "multipart/form-data"
                }
            }
        );

        // Conversation me attach karo
        await axios.post(
            `${API}/conversation/add-pdf`,
            {
                conversation_id: conversation.id,
                pdf_ids: [response.data.pdf_id]
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        // Duplicate check
        const alreadyExists = (conversation.pdfs || []).some(
            pdf => pdf.id === response.data.pdf_id
        );

        const updatedConversation = {
            ...conversation,
            pdfs: alreadyExists
                ? conversation.pdfs
                : [
                    ...(conversation.pdfs || []),
                    {
                        id: response.data.pdf_id,
                        filename: response.data.filename
                    }
                ]
        };

        setSelectedConversation(updatedConversation);

        // Chat me selected pdf bhi update
        setConversationPDFs(updatedConversation.pdfs);

        await fetchChats();

        await fetchPDFs();

        await openConversation(updatedConversation);

        toast.success("Document Uploaded Successfully")

    }
    catch (error) {

        if (handleUnauthorized(error)) return;

        toast.error(
            error.response?.data?.detail || "Upload Failed"
        );
    }
    finally{
        setUploading(false);
    }
}   
    async function deletePDF(id) {
        const result = await Swal.fire({
            title: "Delete Document?",
            text: "This action cannot be undone!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonText: "Yes, Delete",
            cancelButtonText: "Cancel",
            confirmButtonColor: "#d33",
            cancelButtonColor: "#3085d6",
        });

        if (!result.isConfirmed) return;

        try {
            await axios.delete(`${API}/pdf/${id}`, {
                headers: { Authorization: `Bearer ${token}` },
            });

            toast.success("Document Deleted Successfully");
            fetchPDFs();
        } catch (error) {
            if (handleUnauthorized(error)) return;
            toast.error("Delete Failed");
        }
    }
    
    

    
    


    

    async function handleRemovePDF(conversationId, pdfId) {

    try {

        await axios.post(
            `${API}/conversation/remove-pdf`,
            {
                conversation_id: conversationId,
                pdf_id: pdfId
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        toast.success("Document removed successfully");

        // Sidebar update
        await fetchChats();

        // Agar current chat wahi hai
        if (
            selectedConversation &&
            selectedConversation.id === conversationId
        ) {

            const updatedConversation = {
                ...selectedConversation,
                pdfs: selectedConversation.pdfs.filter(
                    pdf => pdf.id !== pdfId
                )
            };

            setSelectedConversation(updatedConversation);

            // Chat ke selected PDFs bhi update
            setConversationPDFs(updatedConversation.pdfs);

            await openConversation(updatedConversation);
        }

    }
    catch (error) {

        if (handleUnauthorized(error)) return;

        toast.error(
            error.response?.data?.detail ||
            "Failed to remove Document"
        );
    }
}

    
    // ==============================
    // Chat Functions
    // ==============================

    async function handleAsk() {
        if (!selectedConversation) {
            toast.error("Please create or open a chat");
            return;
        }

        if (!conversationPDFs || conversationPDFs.length === 0) {
          toast.error("Please attach at least one Document before asking a question.");
          return;
        }
        if (!question.trim()) {
            toast.error("Enter Question");
            return;
        }

        const userQuestion = question;
        setMessages(prev => [...prev, { role: "user", text: userQuestion }]);
        setQuestion("");
        setIsTyping(true);

        try {
            const response = await axios.post(
               `${API}/ask`,
                {
                    question: userQuestion,
                    conversation_id: selectedConversation.id
                },
                {
                    headers: { Authorization: `Bearer ${token}` }
                }
            );

            setMessages(prev => [
                ...prev,
                { role: "ai", text: response.data.chat.answer }
            ]);
            fetchChats();
        } catch (error) {
            if (handleUnauthorized(error)) return;
            toast.error(error.response?.data?.detail || "Failed");
        } finally {
            setIsTyping(false);
        }
    }

    function openHistory(chat) {
        setMessages([
            { role: "user", text: chat.question },
            { role: "ai", text: chat.answer }
        ]);
    }

   

    return (
        <div className="container">
            <Sidebar
                sidebarWidth={sidebarWidth}
                startResize={()=>{
                    isResizing.current=true;
                    document.body.style.cursor = "col-resize";
                     document
                        .querySelector(".sidebar")
                        ?.classList.add("resizing");
                }}
                pdfs={pdfs}
                chats={chats}
                createConversation={createConversation}
                newChatLoading={newChatLoading}
                selectedConversation={selectedConversation}
                setSelectedConversation={setSelectedConversation}
                uploading={uploading}
                fileInputRef={fileInputRef}
                openConversation={openConversation}
                deleteConversation={deleteConversation}
                renameConversation={renameConversation}
                deletingId={deletingId}
                deletePDF={deletePDF}
                openHistory={openHistory}
                logout={logout}
                handleFileSelect={handleFileSelect}
                handleRemovePDF={handleRemovePDF}
            />
            <div className="main-content">

                <div className="pdf-badges">
                    {selectedConversation?.pdfs?.map(pdf => (
                        <div key={pdf.id} className="pdf-badge">
                            📄 {pdf.filename}
                        </div>
                    ))}
                </div>
                <hr />

                <div className="chat-box">
                    {
selectedConversation &&
selectedConversation.pdfs?.length===0 &&
messages.length===0 && (

<div className="empty-chat">

    <div className="empty-chat-content">

        <div className="empty-icon">
            🤖
        </div>

        <h2>How can I help you today?</h2>

        <p>
            Upload a PDF to start asking questions about your documents.
        </p>

        <button
            className="upload-btn"
            disabled={uploading}
            onClick={() => {
                if (!uploading)
                    fileInputRef.current.click();
            }}
        >
            {uploading ? (
                <>
                    <span className="spinner"></span>
                    Uploading...
                </>
            ) : (
                <>📄 Upload PDF</>
            )}
        </button>

    </div>

</div>

)
}

                    {messages.map((msg, index) => (
                        <div key={index} className={`message ${msg.role}`}>
                            <b>{msg.role === "user" ? "👤 You" : "✨ AI"}</b>
                           <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                {typeof msg.text === "string"
                                    ? msg.text
                                    : JSON.stringify(msg.text)}
                            </ReactMarkdown>
                        </div>
                    ))}

                    {isTyping && (
                        <div className="message ai">
                            <b>✨ AI</b>
                            <p>Thinking...</p>
                        </div>
                    )}
                    <div ref={chatEndRef}></div>
                </div>

          
                <input
                    type="file"
                    ref={fileInputRef}
                    hidden
                    accept=".pdf,.txt,.docx"
                    onChange={handleFileSelect}
                />
                <div className="chat-input">
                    <div
                        className={`icon-btn attach-btn ${uploading ? "disabled" : ""}`}
                        onClick={() => {
                            if (!uploading)
                                fileInputRef.current.click();
                        }}
                    >
                        {uploading ? (
                            <span className="spinner"></span>
                        ) : (
                            <Plus size={20} />
                        )}
                    </div>

                    <textarea
                        rows="1"
                        value={question}
                        placeholder="Ask anything..."
                        onChange={(e) => {setQuestion(e.target.value);
                            e.target.style.height="auto";
                            e.target.style.height=e.target.scrollHeight+"px";

                        }}
                        onKeyDown={(e) => {
                            if (e.key === "Enter" && !e.shiftKey) {
                                e.preventDefault();
                                handleAsk();

                                e.target.style.height="44px";
                            }

                        }}
                        style={{
                            resize: "none",
                            overflow: "hidden",
                            minHeight: "44px",
                            maxHeight: "200px"
                        }}
                    />
                    
                         <div className="icon-btn send-btn" onClick={handleAsk}>
                            <ArrowUp size={20} />
                        </div>
                   
                </div>
            </div>
           
        </div>
    );
}

export default Chat;