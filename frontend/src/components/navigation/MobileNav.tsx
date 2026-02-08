import React from 'react';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/Sheet';
import { Button } from '@/components/ui/Button';
import { Menu } from 'lucide-react';
import Link from 'next/link';

type NavItem = {
  label: string;
  href: string;
};

type MobileNavProps = {
  navItems: NavItem[];
  isLoggedIn: boolean;
  onLogout?: () => void;
};

const MobileNav: React.FC<MobileNavProps> = ({ navItems, isLoggedIn, onLogout }) => {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="md:hidden">
          <Menu className="h-5 w-5" />
        </Button>
      </SheetTrigger>
      <SheetContent side="left" className="w-64">
        <div className="flex flex-col space-y-4 mt-8">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href as any}
              className="text-lg font-medium hover:underline"
            >
              {item.label}
            </Link>
          ))}

          {isLoggedIn && onLogout && (
            <Button
              variant="ghost"
              className="justify-start text-left"
              onClick={onLogout}
            >
              Logout
            </Button>
          )}
        </div>
      </SheetContent>
    </Sheet>
  );
};

export { MobileNav };