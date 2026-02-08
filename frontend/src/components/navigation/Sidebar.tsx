import React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { cn } from '@/lib/utils';

type NavItem = {
  label: string;
  href: string;
  icon?: React.ReactNode;
};

type SidebarProps = {
  navItems: NavItem[];
  isLoggedIn: boolean;
  onLogout?: () => void;
  className?: string;
};

const Sidebar: React.FC<SidebarProps> = ({ navItems, isLoggedIn, onLogout, className }) => {
  return (
    <aside className={cn("hidden md:block w-64 border-r p-4", className)}>
      <div className="space-y-2">
        <h2 className="text-xl font-bold mb-6">TodoApp</h2>

        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href as any}
            className="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary"
          >
            {item.icon && item.icon}
            {item.label}
          </Link>
        ))}

        {isLoggedIn && onLogout && (
          <Button
            variant="ghost"
            className="w-full justify-start mt-4"
            onClick={onLogout}
          >
            Logout
          </Button>
        )}
      </div>
    </aside>
  );
};

export { Sidebar };