import './globals.css';
import { ToastProvider } from '@/context/ToastContext';

export const metadata = {
  title: 'Квартиры посуточно',
  description: 'Аренда квартир посуточно',
};

export default function RootLayout({ children }) {
  return (
    <html lang="ru">
      <body>
        <ToastProvider position="top-right">
          {children}
        </ToastProvider>
      </body>
    </html>
  );
}