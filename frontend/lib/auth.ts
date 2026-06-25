import api from './api';
import { User } from '@/types';

export const authService = {
  async register(
    email: string,
    name: string,
    password: string
  ) {
    const res = await api.post(
      '/api/auth/register',
      {
        email,
        name,
        password,
      }
    );

    localStorage.setItem(
      'anchor_token',
      res.data.access_token
    );

    return res.data;
  },

  async login(
    email: string,
    password: string
  ) {
    const res = await api.post(
      '/api/auth/login',
      {
        email,
        password,
      }
    );

    localStorage.setItem(
      'anchor_token',
      res.data.access_token
    );

    return res.data;
  },

  async getMe(): Promise<User> {
    const res = await api.get('/api/auth/me');

    return res.data;
  },

  logout() {
    localStorage.removeItem('anchor_token');

    window.location.href = '/login';
  },

  isAuthenticated() {
    if (typeof window === 'undefined') {
      return false;
    }

    return !!localStorage.getItem('anchor_token');
  },
};