import api from './api';

import { Roadmap } from '@/types';


export const roadmapService = {
  async getAll(): Promise<Roadmap[]> {
    const res = await api.get(
      '/api/roadmaps/'
    );

    return res.data;
  },

  async startRoadmap(
    roadmapId: string
  ) {
    const res = await api.post(
      '/api/user-roadmaps/start',
      {
        roadmap_id: roadmapId,
      }
    );

    return res.data;
  },

  async getMyRoadmaps() {
    const res = await api.get(
      '/api/user-roadmaps/history'
    );

    return res.data;
  },

  async completeStep(
    urId: string,
    stepId: string
  ) {
    const res = await api.post(
      `/api/user-roadmaps/${urId}/complete-step/${stepId}`
    );

    return res.data;
  },

  async updateStatus(
    urId: string,
    status: string
  ) {
    const res = await api.patch(
      `/api/user-roadmaps/${urId}/status`,
      {
        status
      }
    );

    return res.data;
  },

  async saveRoadmap(
    roadmapId: string
  ) {
    const res = await api.post(
      '/api/user-roadmaps/start',
      {
        roadmap_id: roadmapId,
        status: 'saved'
      }
    );

    return res.data;
  },
};