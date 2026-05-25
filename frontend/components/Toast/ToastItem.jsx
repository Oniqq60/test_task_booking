'use client';

import { motion } from 'framer-motion';
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react';
import { TOAST_TYPES } from '@/context/ToastTypes';

const typeConfig = {
  [TOAST_TYPES.SUCCESS]: {
    icon: CheckCircle,
    bgColor: 'bg-green-50',
    borderColor: 'border-green-200',
    textColor: 'text-green-800',
    iconColor: 'text-green-500',
  },
  [TOAST_TYPES.ERROR]: {
    icon: AlertCircle,
    bgColor: 'bg-red-50',
    borderColor: 'border-red-200',
    textColor: 'text-red-800',
    iconColor: 'text-red-500',
  },
  [TOAST_TYPES.WARNING]: {
    icon: AlertTriangle,
    bgColor: 'bg-yellow-50',
    borderColor: 'border-yellow-200',
    textColor: 'text-yellow-800',
    iconColor: 'text-yellow-500',
  },
  [TOAST_TYPES.INFO]: {
    icon: Info,
    bgColor: 'bg-blue-50',
    borderColor: 'border-blue-200',
    textColor: 'text-blue-800',
    iconColor: 'text-blue-500',
  },
};

export default function ToastItem({ toast, onRemove }) {
  const config = typeConfig[toast.type] || typeConfig[TOAST_TYPES.INFO];
  const Icon = config.icon;

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: -20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -20, scale: 0.95, transition: { duration: 0.2 } }}
      className={`flex items-start gap-3 p-4 rounded-lg border shadow-lg ${config.bgColor} ${config.borderColor} ${config.textColor} min-w-[300px] max-w-md`}
      role="alert"
      aria-live="polite"
    >
      <Icon className={`h-5 w-5 flex-shrink-0 mt-0.5 ${config.iconColor}`} />
      
      <p className="flex-1 text-sm font-medium leading-relaxed">
        {toast.message}
      </p>
      
      <button
        onClick={onRemove}
        className={`flex-shrink-0 p-1 rounded hover:bg-black/5 transition-colors ${config.iconColor}`}
        aria-label="Закрыть уведомление"
      >
        <X className="h-4 w-4" />
      </button>
      
      {/* Прогресс-бар */}
      {toast.duration > 0 && (
        <div className="absolute bottom-0 left-0 right-0 h-1 bg-black/5 rounded-b-lg overflow-hidden">
          <motion.div
            className={`h-full ${config.iconColor.replace('text-', 'bg-')}`}
            initial={{ width: '100%' }}
            animate={{ width: '0%' }}
            transition={{ duration: toast.duration / 1000, ease: 'linear' }}
          />
        </div>
      )}
    </motion.div>
  );
}