export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
}

export interface Step {
  id: string;
  roadmap_id: string;
  title: string;
  description: string;
  resource_url: string;
  resource_type: string;
  order: number;
  duration_minutes: number;
}

export interface Roadmap {
  id: string;
  title: string;
  description: string;
  category: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  estimated_hours: number;
  tags: string;
  steps: Step[];
}

export type RoadmapStatus =
  | 'active'
  | 'paused'
  | 'completed'
  | 'abandoned';

export interface UserRoadmap {
  id: string;
  roadmap_id: string;
  user_id: string;
  status: string;
  progress_percentage: number;
  roadmap: Roadmap;
  completed_steps: {step_id: string;}[];
}