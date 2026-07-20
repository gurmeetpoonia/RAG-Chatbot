import { BrowserRouter, Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Chat from "./pages/Chat";

function App() {

    return (

        <BrowserRouter>

            <Routes>

                <Route
                    path="/"
                    element={<Login />}
                />

                <Route
                    path="/register"
                    element={<Register />}
                />

                <Route
                    path="/chat"
                    element={
                        <ProtectedRoute>
                            <Chat />
                        </ProtectedRoute>
                }
                />

            </Routes>

        </BrowserRouter>

    );

}

export default App;