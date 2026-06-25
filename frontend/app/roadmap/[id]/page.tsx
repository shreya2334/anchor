'use client';

import {
  useEffect,
  useState
} from 'react';

import { useParams } from 'next/navigation';

import { roadmapService } from '@/lib/roadmaps';

import {
  Roadmap,
  UserRoadmap
} from '@/types';


export default function RoadmapPage() {
  const params = useParams();

  const [roadmap, setRoadmap] =
    useState<Roadmap | null>(null);

  const [userRoadmap, setUserRoadmap] =
    useState<UserRoadmap | null>(null);

  const [loading, setLoading] =
    useState(true);


  useEffect(() => {
    roadmapService
      .getAll()
      .then((data) => {
        const found = data.find(
          (r) => r.id === params.id
        );

        setRoadmap(found || null);
      });

    roadmapService
      .getMyRoadmaps()
      .then((urs) => {
        const active = urs.find(
          (ur: UserRoadmap) =>
            ur.roadmap.id === params.id
        );

        setUserRoadmap(active || null);
      })
      .finally(() =>
        setLoading(false)
      );

  }, [params.id]);


  if (loading) {
    return (
      <main className='min-h-screen flex items-center justify-center'>
        <p>Loading roadmap...</p>
      </main>
    );
  }


  if (!roadmap) {
    return (
      <main className='min-h-screen flex items-center justify-center'>
        <p>Roadmap not found.</p>
      </main>
    );
  }


  return (
    <main className='min-h-screen bg-stone-50 p-8'>
      <div className='max-w-4xl mx-auto'>

        <div className='mb-10'>
          <h1 className='text-4xl font-bold text-gray-900 mb-3'>
            {roadmap.title}
          </h1>

          <p className='text-gray-500 text-lg'>
            {roadmap.description}
          </p>
        </div>


        <div className='space-y-6'>
          {roadmap.steps.map((step, index) => (
            <div
              key={step.id}
              className='bg-white border border-stone-200 rounded-2xl p-6'
            >
              <div className='flex items-start justify-between gap-4'>

                <div>
                  <p className='text-sm text-blue-600 font-medium mb-2'>
                    Step {index + 1}

                    {
                      userRoadmap?.completed_steps?.some(
                         (cs) =>
                            cs.step_id === step.id
                      ) && (
                        <span className='ml-3 text-green-600'>
                          ✓ Completed
                        </span>
                      )
                    }
                  </p>

                  <h2 className='text-2xl font-semibold text-gray-900 mb-2'>
                    {step.title}
                  </h2>

                  <p className='text-gray-500 mb-4'>
                    {step.description}
                  </p>

                  <div className='flex items-center gap-3 text-sm'>
                    <span className='px-3 py-1 bg-stone-100 rounded-full text-gray-600'>
                      {step.resource_type}
                    </span>

                    <span className='text-gray-500'>
                      {step.duration_minutes}
                      {' '}
                      mins
                    </span>
                  </div>
                </div>


                <div className='flex flex-col gap-3'>
                  <a
                    href={step.resource_url}
                    target='_blank'
                    className='px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-700 transition-colors whitespace-nowrap'
                  >
                    Open Resource
                  </a>

                  {userRoadmap?.status === 'active' && (
                    <button
                      onClick={async () => {
                        await roadmapService.completeStep(
                          userRoadmap.id,
                          step.id
                        );

                        const refreshed =
                          await roadmapService.getMyRoadmaps();

                        const current =
                          refreshed.find(
                            (ur: UserRoadmap) =>
                              ur.roadmap.id === params.id
                          );

                        setUserRoadmap(current || null);
                      }}
                      className='px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors'
                    >
                      Complete Step
                    </button>
                  )}
                </div>

              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}