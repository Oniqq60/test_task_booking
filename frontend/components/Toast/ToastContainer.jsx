'use client';

import ToastItem from './ToastItem'
import { motion, AnimatePresence } from 'framer-motion';

const positionClasses = {
  'top-right': 'top-4 right-4',
  'top-left': 'top-4 left-4',
  'bottom-right': 'bottom-4 right-4',
  'bottom-left': 'bottom-4 left-4',
  'top-center': 'top-4 left-1/2 -translate-x-1/2',
  'bottom-center': 'bottom-4 left-1/2 -translate-x-1/2',
};

export default function ToastContainer({ position = 'top-right', toasts, onRemove }) {
  return (
    <div className={`fixed z-50 flex flex-col gap-2 ${positionClasses[position]}`}>
      <AnimatePresence mode="popLayout">
        {toasts.map((toast) => (
          <ToastItem 
            key={toast.id} 
            toast={toast} 
            onRemove={() => onRemove(toast.id)} 
          />
        ))}
      </AnimatePresence>
    </div>
  );
}