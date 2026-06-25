'use client';

import {
  useEffect,
  useState
} from 'react';

import { useRouter } from 'next/navigation';

import { useAuth } from '../../hooks/useAuth';

import { roadmapService } from '../../lib/roadmaps';

import {
  Roadmap,
  UserRoadmap
} from '@/types';


export default function DashboardPage() {
  const router = useRouter();

  const {
    user,
    loading,
    logout
  } = useAuth();

  const [roadmaps, setRoadmaps] =
    useState<Roadmap[]>([]);

  const [
    activeRoadmaps,
    setActiveRoadmaps
  ] = useState<UserRoadmap[]>([]);

  const [
    loadingRoadmaps,
    setLoadingRoadmaps
  ] = useState(true);

  const active = activeRoadmaps.filter(
    r => r.status === 'active'
  );

  const paused = activeRoadmaps.filter(
    r => r.status === 'paused'
  );
  const saved = activeRoadmaps.filter(
    r => r.status === 'saved'
  );
  const completed = activeRoadmaps.filter(
    r => r.status === 'completed'
  );

  activeRoadmaps.forEach(r =>
    console.log(
      r.roadmap?.title,
      r.status
    )
  );

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [loading, user, router]);


  useEffect(() => {
    roadmapService
      .getAll()
      .then(setRoadmaps)
      .finally(() =>
        setLoadingRoadmaps(false)
      );

    roadmapService
      .getMyRoadmaps()
      .then(setActiveRoadmaps)
      .catch(console.error);

  }, []);


  async function refreshRoadmaps() {
    const updated =
      await roadmapService.getMyRoadmaps();

    setActiveRoadmaps(updated);
  }


  async function handleStart(
    roadmapId: string
  ) {
    try {
      const created =
        await roadmapService.startRoadmap(
          roadmapId
        );

      await refreshRoadmaps();

      if (created.status === 'saved') {
        alert(
          'You already have an active roadmap.\n\nThis roadmap has been saved for later.'
        );
      } else {
        alert(
          'Roadmap started successfully!'
        );
      }

    } catch {
        alert(
          'This roadmap is already in your journey.'
        );
      }
  }


  if (loading) {
    return (
      <main className='min-h-screen flex items-center justify-center'>
        <p className='text-gray-500'>
          Loading...
        </p>
      </main>
    );
  }


  return (
    <main className='min-h-screen bg-[#F8F7F4] px-8 py-10'>
      <div className='max-w-6xl mx-auto'>

        <div className='flex items-start justify-between mb-16'>

          <div>
            <p className='text-slate-500 text-sm uppercase tracking-[0.25em] mb-3'>
              Anchor
            </p>

            <h1 className='text-5xl font-bold text-slate-900 mb-3'>
              Stay Anchored 
            </h1>

            <p className='text-slate-500 text-lg'>
              {
                active.length > 0
                  ? `${active[0].roadmap.title} is underway.`
                  : completed.length > 0
                  ? 'Ready for your next quest.'
                  : 'Finish what you start.'
              }
            </p>

            <p className='text-slate-400 text-sm mt-3 max-w-lg'>
              One roadmap at a time. Steady progress beats scattered effort.
            </p>

            {
              active.length > 0 && (
                <p className='text-sm text-slate-600 mt-3 font-medium'>
                  {active[0].progress_percentage}% completed
                </p>
              )
            }

            <p className='text-slate-400 text-sm mt-2'>
              Welcome back, {user?.name}
            </p>
          </div>

          <button
            onClick={logout}
            className='px-5 py-3 bg-slate-900 text-white rounded-2xl hover:bg-slate-800 transition-all'
          >
            Logout
          </button>

        </div>

        <div className='grid grid-cols-2 md:grid-cols-4 gap-4 mb-12'>

          <div
            onClick={() =>
              document
                .getElementById('active-section')
                ?.scrollIntoView({
                  behavior: 'smooth'
                })
            }
            className='bg-white rounded-3xl p-6 shadow-sm border border-stone-100 hover:border-slate-300 hover:shadow-2xl hover:-translate-y-3 hover:scale-[1.02] transition-all duration-300 cursor-pointer'
          >
            <p className='text-sm font-semibold text-blue-800 mb-2'>
              Active
            </p>      

            <p className='text-5xl font-bold text-slate-900'>
              {active.length}
            </p>

            <p className='text-xs text-slate-400 mt-2'>
              Roadmaps in progress
            </p>
          </div>

          <div
            onClick={() =>
              document
                .getElementById('saved-section')
                ?.scrollIntoView({
                  behavior: 'smooth'
                })
            }
            className='bg-white rounded-3xl p-6 shadow-sm border border-stone-100 hover:border-slate-300 hover:shadow-2xl hover:-translate-y-3 hover:scale-[1.02] transition-all duration-300 cursor-pointer'
          >
            <p className='text-sm font-semibold text-blue-800 mb-2'>
              Saved
            </p>

            <p className='text-5xl font-bold text-slate-900'>
              {saved.length}
            </p>

            <p className='text-xs text-slate-400 mt-2'>
              Ready for later
            </p>
          </div>

          <div
            onClick={() =>
              document
                .getElementById('paused-section')
                ?.scrollIntoView({
                  behavior: 'smooth'
                })
            }
            className='bg-white rounded-3xl p-6 shadow-sm border border-stone-100 hover:border-slate-300 hover:shadow-2xl hover:-translate-y-3 hover:scale-[1.02] transition-all duration-300 cursor-pointer'
          >
            <p className='text-sm font-semibold text-blue-800 mb-2'>
              Paused
            </p>

            <p className='text-5xl font-bold text-slate-900'>
              {paused.length}
            </p>

            <p className='text-xs text-slate-400 mt-2'>
              Anchored temporarily 
            </p>
          </div>

          <div
            onClick={() =>
              document
                .getElementById('completed-section')
                ?.scrollIntoView({
                  behavior: 'smooth'
                })
            }
            className='bg-white rounded-3xl p-6 shadow-sm border border-stone-100 hover:border-slate-300 hover:shadow-2xl hover:-translate-y-3 hover:scale-[1.02] transition-all duration-300 cursor-pointer'
          >
            <p className='text-sm font-semibold text-blue-800 mb-2'>
              Completed
            </p>

            <p className='text-5xl font-bold text-slate-900'>
              {completed.length}
            </p>

            <p className='text-xs text-slate-400 mt-2'>
              Quests Completed
            </p>
          </div>
        </div>

        {active.length > 0 && (
          <div id='active-section' className='mb-12'>
            <h2 className='text-2xl font-semibold text-gray-900 mb-6'>
               Active Roadmaps
            </h2>

            <div className='grid md:grid-cols-2 gap-6'>
              {active.map((ur) => (
                <div
                  key={ur.id}
                  onClick={() =>
                    router.push(`/roadmap/${ur.roadmap.id}`)
                  }
                  className='bg-white rounded-3xl p-7 cursor-pointer shadow-sm border border-stone-100 hover:shadow-lg hover:-translate-y-1 transition-all duration-300'
                >

                  <div className='flex items-center justify-between mb-4'>
                    <h3 className='text-2xl font-semibold text-slate-900'>
                      {ur.roadmap?.title}
                    </h3>

                    <span className='px-3 py-1 bg-slate-100 rounded-full text-sm font-semibold text-slate-700'>
                      {ur.progress_percentage}%
                    </span>
                  </div>


                  <div className='w-full bg-stone-200 rounded-full h-3 mb-4'>
                    <div
                      className='bg-slate-900 h-3 rounded-full transition-all'
                      style={{
                        width: `${ur.progress_percentage}%`
                      }}
                    />
                  </div>


                  <div className='mt-2'>
                    <p className='text-sm text-gray-500'>
                      {ur.completed_steps?.length || 0}
                      {' '}
                      of
                      {' '}
                      {ur.roadmap?.steps?.length || 0}
                      {' '}
                      steps completed
                    </p>

                    <p className='text-sm text-slate-700 mt-2'>
                      {
                        ur.progress_percentage === 0
                          ? 'Your journey starts here.'
                          : ur.progress_percentage < 50
                          ? 'Building momentum.'
                          : ur.progress_percentage < 80
                          ? 'You are halfway there.'
                          : ur.progress_percentage < 100
                          ? 'The finish line is in sight.'
                          : 'Quest completed!'
                      }
                    </p>
                  </div>

                  <p className='text-sm text-slate-700 mt-4 font-medium'>
                    Continue Journey →
                  </p>


                  <div className='mt-4 flex items-center justify-between'>

                    <span
                      className={`
                        px-3 py-1 rounded-full text-xs font-semibold

                        ${
                          ur.status === 'active'
                            ? 'bg-green-100 text-green-700'
                            : ur.status === 'paused'
                            ? 'bg-amber-100 text-amber-700'
                            : ur.status === 'saved'
                            ? 'bg-blue-100 text-blue-700'
                            : 'bg-purple-100 text-purple-700'
                        }
                      `}
                    >
                      {
                        ur.status === 'active'
                          ? 'Active'
                          : ur.status === 'paused'
                          ? 'Paused'
                          : ur.status === 'saved'
                          ? 'Saved'
                          : 'Completed'
                      }
                    </span>


                    {ur.status === 'active' && (
                      <button
                        onClick={async (e) => {
                          e.stopPropagation();

                          try {
                            await roadmapService.updateStatus(
                              ur.id,
                              'paused'
                            );

                            await refreshRoadmaps();

                          } catch {
                            alert(
                              'You already have an active roadmap. \n\nPause or complete it before resuming this one.'
                            );
                          }
                        }}
                        className='px-4 py-2 bg-yellow-500 text-white rounded-lg text-sm hover:bg-yellow-600 transition-colors'
                      >
                        Pause
                      </button>
                    )}


                    {ur.status === 'paused' && (
                      <button
                        onClick={async (e) => {
                          e.stopPropagation();

                          await roadmapService.updateStatus(
                            ur.id,
                            'active'
                          );

                          await refreshRoadmaps();
                        }}
                        className='px-4 py-2 bg-green-600 text-white rounded-lg text-sm hover:bg-green-700 transition-colors'
                      >
                        Resume
                      </button>
                    )}

                  </div>

                </div>
              ))}
            </div>
          </div>
        )}

        {saved.length > 0 && (
          <div id='saved-section' className='mb-12'>
            <h2 className='text-2xl font-semibold text-slate-900 mb-6'>
              Saved For Later
            </h2>

            <div className='grid md:grid-cols-2 gap-6'>
              {saved.map((ur) => (
                <div
                  key={ur.id}
                  onClick={() =>
                    router.push(`/roadmap/${ur.roadmap.id}`)
                  }
                  className='bg-white rounded-3xl p-6 shadow-sm border border-stone-100 cursor-pointer hover:shadow-xl hover:-translate-y-2 transition-all duration-300'
                >
                <h3 className='text-xl font-semibold text-slate-900'>
                  {ur.roadmap.title}
                </h3>

                <div className='mt-3'>
                  <span className='px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-semibold'>
                    Saved
                  </span>
                </div>

                <div className='mt-4 flex items-center justify-between'>

                  <p className='text-slate-500'>
                    Ready whenever you are.
                  </p>

                  <button
                    onClick={async (e) => {
                      e.stopPropagation();

                      try {
                        await roadmapService.updateStatus(
                          ur.id,
                          'active'
                        );

                        await refreshRoadmaps();

                      } catch {
                        alert(
                          'You already have an active roadmap. \n\nPause or complete it first.'
                        );
                      }
                    }}
                    className='px-4 py-2 bg-slate-900 text-white rounded-xl text-sm hover:bg-slate-700 transition-colors'
                  >
                    Start Now
                  </button>

                </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {paused.length > 0 && (
          <div id='paused-section' className='mb-12'>
            <h2 className='text-2xl font-semibold text-slate-900 mb-6'>
              Paused
            </h2>

            <div className='grid md:grid-cols-2 gap-6'>
              {paused.map((ur) => (
                <div
                  key={ur.id}
                  onClick={() =>
                    router.push(`/roadmap/${ur.roadmap.id}`)
                  }
                  className='bg-white rounded-3xl p-6 shadow-sm border border-stone-100 cursor-pointer hover:shadow-xl hover:-translate-y-2 transition-all duration-300'
                >
                  <h3 className='text-xl font-semibold text-slate-900'>
                    {ur.roadmap.title}
                  </h3>

                  <div className='mt-3'>
                    <span className='px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-xs font-semibold'>
                      Paused
                    </span>
                  </div>

                  <div className='mt-4 flex items-center justify-between'>

                    <p className='text-slate-500'>
                      Resume whenever you are ready.
                    </p>

                    <button
                      onClick={async (e) => {
                        e.stopPropagation();

                        await roadmapService.updateStatus(
                          ur.id,
                          'active'
                        );

                        await refreshRoadmaps();
                      }}
                      className='px-4 py-2 bg-slate-900 text-white rounded-xl text-sm hover:bg-slate-700 transition-colors'
                    >
                      Resume
                    </button>

                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {completed.length > 0 && (
          <div id='completed-section' className='mb-12'>
            <h2 className='text-2xl font-semibold text-slate-900 mb-6'>
              Completed
            </h2>

            <div className='grid md:grid-cols-2 gap-6'>
              {completed.map((ur) => (
                <div
                  key={ur.id}
                  className='bg-white rounded-3xl p-6 shadow-sm border border-stone-100'
                >
                  <h3 className='text-xl font-semibold text-slate-900'>
                    {ur.roadmap.title}
                  </h3>

                  <div className='mt-3'>
                    <span className='px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-semibold'>
                      Completed
                    </span>
                  </div>

                  <p className='text-emerald-600 mt-2 font-medium'>
                    Completed successfully!
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className='mb-8'>
          <h2 className='text-2xl font-semibold text-gray-900 mb-2'>
            Discover Roadmaps
          </h2>

          <p className='text-gray-500'>
            Choose one path and commit to it.
          </p>
        </div>


        {loadingRoadmaps ? (
          <p className='text-gray-500'>
            Loading roadmaps...
          </p>

        ) : (
          <div className='grid md:grid-cols-2 lg:grid-cols-3 gap-6'>
            {roadmaps.map((roadmap) => (
              <div
                key={roadmap.id}
                onClick={() =>
                  router.push(`/roadmap/${roadmap.id}`)
                }
                className='bg-white rounded-3xl p-7 cursor-pointer shadow-sm border border-stone-100 hover:shadow-xl hover:-translate-y-2 transition-all duration-300'
              >

                <div className='mb-4'>
                  <h3 className='text-xl font-semibold text-gray-900 mb-2'>
                    {roadmap.title}
                  </h3>

                  <p className='text-gray-500 text-sm'>
                    {roadmap.description}
                  </p>
                </div>


                <div className='flex items-center gap-2 mb-4'>
                  <span className='px-2 py-1 bg-stone-100 rounded text-xs text-gray-600'>
                    {roadmap.category}
                  </span>

                  <span className='px-2 py-1 bg-blue-100 rounded text-xs text-blue-700'>
                    {roadmap.difficulty}
                  </span>
                </div>


                <div className='text-sm text-gray-500 mb-6'>
                  {roadmap.estimated_hours}
                  {' '}
                  hours •
                  {' '}
                  {roadmap.steps.length}
                  {' '}
                  steps
                </div>


                <button
                  onClick={(e) => {
                    e.stopPropagation();

                    handleStart(roadmap.id);
                  }}
                  className='w-full bg-gray-900 text-white py-3 rounded-lg font-medium hover:bg-gray-700 transition-colors'
                >
                  Start Roadmap
                </button>

              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}