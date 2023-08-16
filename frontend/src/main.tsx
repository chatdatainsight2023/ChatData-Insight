import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import Home from './Home';
import './main.css';
import './i18n';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/home",
    element: <Home/>
  },
  {
    path: "/",
    element: <App/>
  }
]);

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
