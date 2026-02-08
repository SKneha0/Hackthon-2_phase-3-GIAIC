import React from 'react';
import Link from 'next/link';

type AuthLayoutProps = {
  children: React.ReactNode;
  title: string;
  description: string;
  footerText: string;
  footerLinkText: string;
  footerLinkHref: string;
};

const AuthLayout: React.FC<AuthLayoutProps> = ({
  children,
  title,
  description,
  footerText,
  footerLinkText,
  footerLinkHref,
}) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-muted p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold">{title}</h1>
          <p className="text-muted-foreground mt-2">{description}</p>
        </div>

        <div className="bg-card rounded-lg shadow p-6">
          {children}
        </div>

        <div className="mt-6 text-center text-sm text-muted-foreground">
          <p>
            {footerText}{' '}
            <Link href={footerLinkHref as any} className="text-primary hover:underline">
              {footerLinkText}
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export { AuthLayout };