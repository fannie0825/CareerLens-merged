import { useState, useCallback } from 'react';

/**
 * Toast Notification Hook
 * Manages toast notifications throughout the application
 */

const TOAST_DURATION = 3000; // 3 seconds

export const useToast = () => {
  const [toasts, setToasts] = useState([]);

  const showToast = useCallback((message, type = 'info') => {
    const id = Date.now() + Math.random();
    const toast = {
      id,
      message,
      type, // 'success', 'error', 'warning', 'info'
    };

    setToasts((prev) => [...prev, toast]);

    // Auto remove after duration
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, TOAST_DURATION);

    return id;
  }, []);

  const removeToast = useCallback((id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const success = useCallback((message) => showToast(message, 'success'), [showToast]);
  const error = useCallback((message) => showToast(message, 'error'), [showToast]);
  const warning = useCallback((message) => showToast(message, 'warning'), [showToast]);
  const info = useCallback((message) => showToast(message, 'info'), [showToast]);

  return {
    toasts,
    showToast,
    removeToast,
    success,
    error,
    warning,
    info,
  };
};
