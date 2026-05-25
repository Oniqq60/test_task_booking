'use client';

import { createContext, useContext, useState, useCallback } from 'react';
import ToastContainer from '../components/Toast/ToastContainer';
import { TOAST_TYPES, TOAST_POSITIONS } from './ToastTypes'; // ← Импортируем из отдельного файла

const DEFAULT_DURATION = 4000;

const ToastContext = createContext(null);

export function ToastProvider({ children, position = TOAST_POSITIONS.TOP_RIGHT }) {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((message, type = TOAST_TYPES.INFO, options = {}) => {
    const id = crypto.randomUUID();
    const toast = {
      id,
      message,
      type,
      duration: options.duration ?? DEFAULT_DURATION,
      position: options.position ?? position,
      onClose: options.onClose,
    };

    setToasts((prev) => [...prev, toast]);

    if (toast.duration > 0) {
      setTimeout(() => {
        removeToast(id);
      }, toast.duration);
    }

    return id;
  }, [position]);

  const removeToast = useCallback((id) => {
    setToasts((prev) => {
      const toast = prev.find((t) => t.id === id);
      if (toast?.onClose) {
        toast.onClose();
      }
      return prev.filter((t) => t.id !== id);
    });
  }, []);

  const clearToasts = useCallback(() => {
    setToasts([]);
  }, []);

  const toastsByPosition = toasts.reduce((acc, toast) => {
    const pos = toast.position;
    if (!acc[pos]) acc[pos] = [];
    acc[pos].push(toast);
    return acc;
  }, {});

  return (
    <ToastContext.Provider value={{ addToast, removeToast, clearToasts, toasts }}>
      {children}
      
      {/* Контейнеры для каждой позиции */}
      {Object.entries(toastsByPosition).map(([pos, positionToasts]) => (
        <ToastContainer 
          key={pos} 
          position={pos} 
          toasts={positionToasts} 
          onRemove={removeToast} 
        />
      ))}
    </ToastContext.Provider>
  );
}

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within ToastProvider');
  }
  return context;
}

export { TOAST_TYPES, TOAST_POSITIONS };