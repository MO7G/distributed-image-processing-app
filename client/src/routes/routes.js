// src/routes.js
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ImageUpload from '../component/ImageUpload/imageUpload';
const MainRoutes = ({ isAuthenticated , setIsAuthenticated }) => {
    return (
        <Routes>
           <Route path="/" element={<h1>Hello home is here</h1>}/>
           <Route path="/uploadImage" element={<ImageUpload></ImageUpload>}/>

            <Route path="*" element={<h1>not found</h1>} />
            
        </Routes>
    );
};

export default MainRoutes;