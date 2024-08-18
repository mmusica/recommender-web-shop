import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser } from '../api/api';  // Import the function from your API service
import { useAuth } from '../context/AuthContext';

function LoginPage() {
    const { setUserId } = useAuth();
    const [username, setUsername] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        try {
            const response = await loginUser(username);
            const userId = response;

            if (userId) {
                setUserId(userId);
                console.log('Login successful:', userId);
                navigate('/recommendations');
            } else {
                console.error('Login failed: No user ID returned');
            }
        } catch (error) {
            console.error('Login failed:', error);
        }
    };

    return (
        <div className="container mt-5">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label htmlFor="username" className="form-label">Username</label>
                    <input
                        type="text"
                        className="form-control"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="btn btn-primary">Login</button>
            </form>
        </div>
    );
};

export default LoginPage;
