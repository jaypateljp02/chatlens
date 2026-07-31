import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';
import MobileBottomNav from './MobileBottomNav';
import './Layout.css';

export default function Layout({ children }) {
  return (
    <div className="layout" id="app-layout">
      <Sidebar />
      <main className="main-content">
        <Header />
        <div className="content-wrapper scroll-area">
          {children || <Outlet />}
        </div>
      </main>
      <MobileBottomNav />
    </div>
  );
}
