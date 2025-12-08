/**
 * Example usage of the CareerLens Dashboard
 * 
 * This file demonstrates how to use the DashboardLayout component
 * in your application.
 */

import React from 'react';
import DashboardLayout from './DashboardLayout';

// Example: Basic usage
export const BasicDashboard = () => {
  return <DashboardLayout />;
};

// Example: With custom dark mode control
export const DashboardWithThemeControl = () => {
  const [darkMode, setDarkMode] = React.useState(false);

  React.useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  return (
    <div>
      <button onClick={() => setDarkMode(!darkMode)}>
        Toggle Dark Mode
      </button>
      <DashboardLayout />
    </div>
  );
};

export default BasicDashboard;
