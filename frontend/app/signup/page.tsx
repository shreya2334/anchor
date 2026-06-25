'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { authService } from '@/lib/auth';

export default function SignupPage() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  async function handleSignup(
    e: React.FormEvent
  ) {
    e.preventDefault();
    setError('');
    setLoading(true);

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    try {
      await authService.register(
        email,
        name,
        password
      );

      router.push('/dashboard');

    } catch {
      setError('Signup failed');

    } finally {
      setLoading(false);
    }
  }


  return (
    <main className='min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-indigo-50 px-6'>
      <div className='w-full max-w-md bg-white border border-stone-200 rounded-2xl p-8 shadow-sm'>
        <h1 className='text-3xl font-bold text-gray-900 mb-2'>
          Create account
        </h1>

        <p className='text-gray-500 mb-8'>
          Start focusing again.
        </p>

        <form
          onSubmit={handleSignup}
          className='space-y-4'
        >
          <input
            type='text'
            placeholder='Name'
            value={name}
            onChange={(e) =>
              setName(e.target.value)
            }
            className='w-full border border-stone-300 rounded-lg px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500'
            required
          />

          <input
            type='email'
            placeholder='Email'
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            className='w-full border border-stone-300 rounded-lg px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500'
            required
          />

          <div className='relative'>
            <input
              type={showPassword ? 'text' : 'password'}
              placeholder='Password'
              value={password}
              onChange={(e) =>
                setPassword(e.target.value)
              }
              className='w-full border border-stone-300 rounded-lg px-4 py-3 pr-16 outline-none focus:ring-2 focus:ring-blue-500'
              required
            />

            <button
              type='button'
              onClick={() =>
                setShowPassword(!showPassword)
              }
              className='absolute right-4 top-1/2 -translate-y-1/2 text-sm text-slate-500 hover:text-slate-700'
            >
              {showPassword ? 'Hide' : 'Show'}
            </button>
          </div>
          
          <div className='relative'>
            <input
              type={showConfirmPassword ? 'text' : 'password'}
              placeholder='Confirm Password'
              value={confirmPassword}
              onChange={(e) =>
                setConfirmPassword(e.target.value)
              }
              className='w-full border border-stone-300 rounded-lg px-4 py-3 pr-16 outline-none focus:ring-2 focus:ring-blue-500'
              required
            />

            <button
              type='button'
              onClick={() =>
                setShowConfirmPassword(
                  !showConfirmPassword
                )
              }
              className='absolute right-4 top-1/2 -translate-y-1/2 text-sm text-slate-500 hover:text-slate-700'
            >
              {showConfirmPassword ? 'Hide' : 'Show'}
            </button>
          </div>
          
          {error && (
            <div className='text-red-500 text-sm'>
              {error}
            </div>
          )}

          <button
            type='submit'
            disabled={loading}
            className='w-full bg-gray-900 text-white py-3 rounded-lg font-medium hover:bg-gray-700 transition-colors disabled:opacity-50'
          >
            {loading
              ? 'Creating account...'
              : 'Create Account'}
          </button>
        </form>

        <p className='text-sm text-gray-500 mt-6 text-center'>
          Already have an account?{' '}

          <Link
            href='/login'
            className='text-blue-600 hover:underline'
          >
            Sign in
          </Link>
        </p>
      </div>
    </main>
  );
}