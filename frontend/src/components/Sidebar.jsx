import React, { useState, useRef, useEffect } from "react";
import { Menu, FileText, Trash2, LogOut, MoreVertical, Pencil, Plus } from "lucide-react";

function Sidebar({
    sidebarWidth,
    startResize,
    pdfs,
    chats,
    newChatLoading,
    createConversation,
    selectedConversation,
    setSelectedConversation,
    uploading,
    fileInputRef,
    renameConversation,
    deleteConversation,
    openConversation,
    logout,
    handleFileSelect,
    handleRemovePDF 
}) {
    const [isOpen, setIsOpen] = useState(true);
    const [openMenu, setOpenMenu] = useState(null);
    
    useEffect(() => {
        function closeMenu() { setOpenMenu(null); }
        window.addEventListener("click", closeMenu);
        return () => window.removeEventListener("click", closeMenu);
    }, []);

    return (
        <div className={`sidebar ${isOpen ? "open" : "close"}`}style={{
            width: sidebarWidth + "px"
            }}
        >
            <div className="sidebar-top">
                <button className="menu-btn" onClick={() => setIsOpen(!isOpen)}>
                    <Menu size={22} />
                </button>
                {isOpen && <h2 className="logo">RAG AI</h2>}
            </div>


            <button
                className="new-chat-btn"
                onClick={createConversation}
                disabled={newChatLoading}
            >
                {newChatLoading ? (
                    <>
                        <span className="spinner"></span>
                        Creating...
                    </>
                ) : (
                    <>
                        ➕ New Chat
                    </>
                )}
            </button>

            <div className="conversation-list">
                {chats.map(chat => (
                    <div
                        key={chat.id}
                        className={`conversation-card ${selectedConversation?.id === chat.id ? "active" : ""}`}
                    >
                        <div className="conversation-header">
                            <div className="conversation-title" onClick={() => openConversation(chat)}>
                                💬 {chat.title}
                            </div>
                            <button
                                className="history-menu-btn"
                                onClick={(e) => {
                                    e.stopPropagation();
                                    setOpenMenu(openMenu === chat.id ? null : chat.id);
                                }}
                            >
                                <MoreVertical size={18} />
                            </button>
                        </div>

                        <div className="conversation-pdfs">
                            {chat.pdfs?.map(pdf => (
                                <div key={pdf.id} className="attached-pdf" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                    <span>📎 {pdf.filename}</span>
                                    {/* PDF Remove Button */}
                                    <button 
                                        className="remove-pdf-btn"
                                        title="Remove PDF from chat"
                                        onClick={(e) => {
                                            e.stopPropagation(); // Chat open hone se rokne ke liye
                                            if (window.confirm(`Remove ${pdf.filename} from this chat?`)) {
                                                // Yahan Chat.jsx se mila hua handleRemovePDF function call hoga
                                                handleRemovePDF(chat.id, pdf.id); 
                                            }
                                        }}
                                        style={{ background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', padding: '2px' }}
                                    >
                                        ✕
                                    </button>
                                </div>
                            ))}
                        </div>
                        {openMenu === chat.id && (
                            <div className="history-menu" onClick={(e) => e.stopPropagation()}>
                                <button onClick={() => renameConversation(chat)}>
                                    <Pencil size={16} /> Rename
                                </button>

                                <button
                                    disabled={uploading}
                                    onClick={() => {
                                        if (uploading) return;

                                        setOpenMenu(null);
                                        setSelectedConversation(chat);
                                        fileInputRef.current.click();
                                    }}
                                >
                                    {uploading ? (
                                        <>
                                            <span className="spinner"></span>
                                            Uploading...
                                        </>
                                    ) : (
                                        <>
                                            <Plus size={16} /> Upload from PC
                                        </>
                                    )}
                                </button>

                                <button onClick={() => deleteConversation(chat.id)}>
                                    <Trash2 size={16} /> Delete
                                </button>
                            </div>
                        )}
                    </div>
                ))}
            </div>
            <div className="logout-section">
            <button className="logout-btn" onClick={logout}>
                <LogOut size={18} />
                {isOpen && <span>Logout</span>}
            </button>
            </div>
            <div
                className="resize-bar"
                onMouseDown={startResize}
            />
            </div>
    );
}

export default Sidebar;