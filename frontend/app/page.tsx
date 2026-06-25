'use client';

import { useEffect } from 'react';

import Link from 'next/link';

import { useRouter } from 'next/navigation';

import { authService } from '@/lib/auth';


export default function LandingPage() {
  const router = useRouter();

  useEffect(() => {
    if (authService.isAuthenticated()) {
      router.push('/dashboard');
    }
  }, [router]);

  return (
    <main className='min-h-screen bg-stone-50 flex flex-col items-center justify-center px-6'>
      <div className='text-center max-w-2xl'>
        <span className='text-6xl mb-8 block'>
          ⚓
        </span>

        <h1 className='text-5xl font-bold text-gray-900 mb-4 tracking-tight'>
          Anchor
        </h1>

        <p className='text-xl text-gray-500 mb-2'>
          For when learning starts to drift.
        </p>

        <p className='text-gray-400 mb-12'>
          One roadmap at a time. Finish what you start.
        </p>

        <div className='flex gap-4 justify-center'>
          <Link
            href='/signup'
            className='px-8 py-3 bg-gray-900 text-white rounded-lg font-medium hover:bg-gray-700 transition-colors'
          >
            Get Started
          </Link>

          <Link
            href='/login'
            className='px-8 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-100 transition-colors'
          >
            Sign In
          </Link>
        </div>
      </div>
    </main>
  );
}