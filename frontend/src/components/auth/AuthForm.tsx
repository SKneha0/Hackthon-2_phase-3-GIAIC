import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { AuthInput } from '@/components/auth/AuthInput';
import { useRouter } from 'next/navigation';
import { useAuthContext } from '@/providers/AuthProvider';

type AuthFormType = 'login' | 'register';

type AuthFormProps = {
  type: AuthFormType;
};

const AuthForm: React.FC<AuthFormProps> = ({ type }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: type === 'register' ? '' : undefined,
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  const { login, register } = useAuthContext();
  const router = useRouter();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, [id]: value }));

    // Clear error when user starts typing
    if (errors[id]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[id];
        return newErrors;
      });
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    if (type === 'register' && !formData.name?.trim()) {
      newErrors.name = 'Name is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    setIsLoading(true);

    try {
      let result;
      if (type === 'login') {
        result = await login(formData.email, formData.password);
      } else {
        result = await register(formData.email, formData.password, formData.name!);
      }

      if (!result.success) {
        if (result.error.includes('Invalid credentials')) {
          setErrors({ credentials: 'Invalid email or password' });
        } else if (result.error.includes('exists')) {
          setErrors({ email: 'Email already exists' });
        } else {
          setErrors({ form: result.error });
        }
      }
    } catch (error) {
      setErrors({ form: 'An unexpected error occurred' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="text-center">
        <CardTitle className="text-2xl font-bold">
          {type === 'login' ? 'Login' : 'Sign Up'}
        </CardTitle>
        <CardDescription>
          {type === 'login'
            ? 'Enter your credentials to access your account'
            : 'Create an account to get started'}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          {type === 'register' && (
            <AuthInput
              label="Full Name"
              id="name"
              type="text"
              placeholder="John Doe"
              value={formData.name || ''}
              onChange={handleChange}
              error={errors.name}
              required
            />
          )}

          <AuthInput
            label="Email"
            id="email"
            type="email"
            placeholder="john@example.com"
            value={formData.email}
            onChange={handleChange}
            error={errors.email}
            required
          />

          <AuthInput
            label="Password"
            id="password"
            type="password"
            placeholder="••••••••"
            value={formData.password}
            onChange={handleChange}
            error={errors.password}
            required
          />

          {errors.credentials && (
            <p className="text-sm text-red-500">{errors.credentials}</p>
          )}

          {errors.form && (
            <p className="text-sm text-red-500">{errors.form}</p>
          )}

          <Button
            type="submit"
            className="w-full mt-4"
            disabled={isLoading}
          >
            {isLoading ? 'Processing...' : (type === 'login' ? 'Login' : 'Sign Up')}
          </Button>
        </form>

        <div className="mt-4 text-center text-sm text-muted-foreground">
          {type === 'login' ? (
            <p>
              Don't have an account?{' '}
              <a href="/signup" className="text-primary hover:underline">
                Sign up
              </a>
            </p>
          ) : (
            <p>
              Already have an account?{' '}
              <a href="/login" className="text-primary hover:underline">
                Login
              </a>
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export { AuthForm };