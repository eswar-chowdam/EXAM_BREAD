import { useEffect, useRef, useState } from 'react'
import { motion } from 'framer-motion'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import {
  analyzeUploadedPdf,
  generateStudyPlan,
  getCurrentUser,
  loginUser,
  registerUser,
} from './api'

const steps = ['PYQs Uploaded', 'Topic Analysis', 'Priority Engine', '7-Day Plan']

export default function App() {
  const [analysis, setAnalysis] = useState(null)
  const [plan, setPlan] = useState(null)
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')
  const [authMode, setAuthMode] = useState('login')
  const [authForm, setAuthForm] = useState({ full_name: '', email: '', password: '' })
  const [user, setUser] = useState(null)
  const fileInputRef = useRef(null)

  useEffect(() => {
    async function loadData() {
      try {
        const currentUser = await getCurrentUser()
        if (currentUser) {
          setUser(currentUser)
        }
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [])

  const handleAuthSubmit = async (event) => {
    event.preventDefault()
    try {
      const payload = {
        full_name: authForm.full_name,
        email: authForm.email,
        password: authForm.password,
      }

      const result = authMode === 'register'
        ? await registerUser(payload)
        : await loginUser({ email: authForm.email, password: authForm.password })

      const currentUser = await getCurrentUser()
      setUser(currentUser)
      setError('')
      setAuthForm({ full_name: '', email: '', password: '' })
    } catch (err) {
      setError(err.message)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('exam_bread_token')
    setUser(null)
  }

  const handleFileUpload = async (event) => {
    const file = event.target.files?.[0]
    if (!file) return

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setError('Please upload a PDF file.')
      return
    }

    setUploading(true)
    setError('')

    try {
      const result = await analyzeUploadedPdf(file)
      setAnalysis(result)

      const generatedPlan = await generateStudyPlan(result)
      setPlan(generatedPlan)
    } catch (err) {
      setError(err.message)
    } finally {
      setUploading(false)
      event.target.value = ''
    }
  }

  const stats = analysis
    ? [
        { label: 'Questions Detected', value: String(analysis.total_questions ?? 0) },
        { label: 'Topics Identified', value: String(Object.keys(analysis.topics ?? {}).length) },
        { label: 'Top Topic', value: analysis.most_frequent_topic ?? 'N/A' },
        { label: 'Study Plan', value: '7-Day' }
      ]
    : [
        { label: 'Questions Detected', value: '0' },
        { label: 'Topics Identified', value: '0' },
        { label: 'Top Topic', value: 'N/A' },
        { label: 'Study Plan', value: '7-Day' }
      ]

  const topicEntries = analysis?.topics
    ? Object.entries(analysis.topics).map(([topic, details]) => ({
        topic,
        frequency: details.count,
        priority: details.priority ?? Math.min(98, 45 + details.count * 12),
      })).sort((a, b) => b.priority - a.priority)
    : []

  const planDays = plan?.days ?? [
    { day: 1, topic: 'Awaiting Upload', duration_minutes: 0, learn: ['Upload a PDF to see topics'], practice: 0, quiz: 0 },
    { day: 2, topic: 'Awaiting Upload', duration_minutes: 0, learn: ['Upload a PDF to see topics'], practice: 0, quiz: 0 },
    { day: 3, topic: 'Awaiting Upload', duration_minutes: 0, learn: ['Upload a PDF to see topics'], practice: 0, quiz: 0 },
    { day: 4, topic: 'Awaiting Upload', duration_minutes: 0, learn: ['Upload a PDF to see topics'], practice: 0, quiz: 0 },
    { day: 5, topic: 'Awaiting Upload', duration_minutes: 0, learn: ['Upload a PDF to see topics'], practice: 0, quiz: 0 },
    { day: 6, topic: 'Awaiting Upload', duration_minutes: 0, learn: ['Upload a PDF to see topics'], practice: 0, quiz: 0 },
    { day: 7, topic: 'Awaiting Upload', duration_minutes: 0, learn: ['Upload a PDF to see topics'], practice: 0, quiz: 0 }
  ]

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,#1f2937_0%,#0f172a_30%,#020617_70%)] text-slate-100">
      <header className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-amber-300 via-orange-400 to-yellow-500 text-lg font-black text-slate-950 shadow-glow">
            B
          </div>
          <div>
            <div className="text-xs uppercase tracking-[0.32em] text-slate-400">EXAM</div>
            <div className="text-xl font-semibold tracking-tight">BREAD</div>
          </div>
        </div>

        <nav className="hidden items-center gap-8 text-sm text-slate-300 md:flex">
          <a href="#product" className="transition hover:text-white">Product</a>
          <a href="#how-it-works" className="transition hover:text-white">How it works</a>
          <a href="#demo" className="transition hover:text-white">Demo</a>
        </nav>

        <div className="flex items-center gap-3">
          {user ? (
            <>
              <span className="hidden rounded-full border border-white/10 bg-white/5 px-3 py-2 text-xs text-slate-200 sm:block">
                {user.full_name}
              </span>
              <button
                onClick={handleLogout}
                className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm font-medium text-white/90 backdrop-blur transition hover:border-amber-300/40 hover:bg-white/10"
              >
                Log out
              </button>
            </>
          ) : (
            <button
              onClick={() => setAuthMode('login')}
              className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm font-medium text-white/90 backdrop-blur transition hover:border-amber-300/40 hover:bg-white/10"
            >
              Sign in
            </button>
          )}
          <button
            onClick={() => fileInputRef.current?.click()}
            className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm font-medium text-white/90 backdrop-blur transition hover:border-amber-300/40 hover:bg-white/10"
          >
            {uploading ? 'Analyzing...' : 'Analyze My PYQs'}
          </button>
        </div>
        <input
          ref={fileInputRef}
          type="file"
          accept="application/pdf"
          className="hidden"
          onChange={handleFileUpload}
        />
      </header>

      <main className="mx-auto max-w-7xl px-6 pb-20 pt-8 lg:px-8">
        <section className="grid items-center gap-12 pb-24 pt-8 lg:grid-cols-[1.1fr_0.9fr]">
          <div>
            <motion.div
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="mb-6 inline-flex items-center gap-2 rounded-full border border-amber-400/20 bg-amber-400/10 px-3 py-1 text-[11px] font-medium uppercase tracking-[0.25em] text-amber-200"
            >
              SMART EXAM PREP
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.08, duration: 0.6 }}
              className="max-w-xl text-5xl font-black tracking-[-0.06em] text-white sm:text-6xl"
            >
              Stop studying everything.
              <span className="mt-2 block bg-gradient-to-r from-amber-200 via-orange-300 to-yellow-500 bg-clip-text text-transparent">
                Start studying what matters.
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.15, duration: 0.6 }}
              className="mt-6 max-w-xl text-lg leading-8 text-slate-300"
            >
              Upload your previous-year papers. Discover the topics that matter most. Get a personalized 7-day preparation plan built around your actual weak points.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.22, duration: 0.6 }}
              className="mt-8 flex flex-wrap items-center gap-4"
            >
              <button
                onClick={() => fileInputRef.current?.click()}
                className="rounded-full bg-gradient-to-r from-amber-300 via-orange-400 to-yellow-500 px-6 py-3 font-semibold text-slate-950 shadow-[0_12px_30px_rgba(251,191,36,0.42)] transition hover:scale-[1.01]"
              >
                {uploading ? 'Analyzing PDF...' : 'Analyze My PYQs'}
              </button>
              <button className="rounded-full border border-white/10 bg-white/5 px-6 py-3 font-semibold text-white transition hover:border-white/20 hover:bg-white/10">
                See How It Works
              </button>
            </motion.div>

            <div className="mt-10 grid max-w-lg grid-cols-2 gap-4 sm:grid-cols-4">
              {stats.map((stat) => (
                <div key={stat.label} className="rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur-sm">
                  <div className="text-2xl font-bold text-white">{stat.value}</div>
                  <div className="mt-1 text-xs uppercase tracking-[0.18em] text-slate-400">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>

          <motion.div
            initial={{ opacity: 0, scale: 0.96 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.15, duration: 0.7 }}
            className="relative"
          >
            <div className="rounded-[28px] border border-white/10 bg-slate-900/80 p-5 shadow-glow backdrop-blur-xl">
              <div className="rounded-[22px] border border-white/10 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 p-5">
                <div className="mb-5 flex items-center justify-between">
                  <div>
                    <p className="text-[10px] uppercase tracking-[0.28em] text-slate-500">PREPARATION FLOW</p>
                    <h2 className="mt-2 text-xl font-semibold text-white">Exam Bread Pipeline</h2>
                  </div>
                  <div className="rounded-full border border-emerald-400/20 bg-emerald-500/10 px-2 py-1 text-xs font-medium text-emerald-300">
                    {loading ? 'Loading' : 'Live'}
                  </div>
                </div>

                <div className="space-y-4">
                  {steps.map((step, index) => (
                    <div key={step} className="flex items-center gap-4">
                      <div className="flex h-10 w-10 items-center justify-center rounded-full border border-amber-300/30 bg-amber-400/10 text-sm font-bold text-amber-200">
                        {index + 1}
                      </div>
                      <div className="flex-1 rounded-2xl border border-white/10 bg-white/[0.02] px-4 py-3 text-sm text-slate-200">
                        {step}
                      </div>
                      {index < steps.length - 1 && (
                        <div className="text-slate-500">↓</div>
                      )}
                    </div>
                  ))}
                </div>

                <div className="mt-6 grid gap-4 sm:grid-cols-2">
                  <div className="rounded-2xl border border-amber-400/20 bg-amber-400/10 p-4">
                    <div className="text-xs uppercase tracking-[0.22em] text-amber-200/70">Priority</div>
                    <div className="mt-3 text-3xl font-black text-white">{topicEntries[0]?.priority ? Math.round(topicEntries[0].priority) : 'N/A'}</div>
                    <div className="mt-1 text-sm text-amber-100">{topicEntries[0]?.topic ?? 'Awaiting Upload'}</div>
                  </div>
                  <div className="rounded-2xl border border-cyan-400/20 bg-cyan-400/10 p-4">
                    <div className="text-xs uppercase tracking-[0.22em] text-cyan-200/70">Readiness</div>
                    <div className="mt-3 text-3xl font-black text-white">
                      {analysis ? `${Math.min(95, Math.max(35, 100 - (Object.keys(analysis.topics ?? {}).length * 7)))}%` : 'N/A'}
                    </div>
                    <div className="mt-1 text-sm text-cyan-100">Exam readiness</div>
                  </div>
                </div>

                {error && (
                  <div className="mt-4 rounded-xl border border-red-500/20 bg-red-500/10 p-3 text-sm text-red-200">
                    {error}
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        </section>

        {!user && (
          <section className="mt-10 rounded-[32px] border border-white/10 bg-slate-900/60 p-6 backdrop-blur-xl">
            <div className="mb-5 flex items-center justify-between gap-4">
              <h3 className="text-2xl font-bold">Student access</h3>
              <div className="flex rounded-full border border-white/10 bg-white/5 p-1">
                <button
                  onClick={() => setAuthMode('login')}
                  className={`rounded-full px-4 py-2 text-sm ${authMode === 'login' ? 'bg-amber-400 text-slate-900' : 'text-white'}`}
                >
                  Login
                </button>
                <button
                  onClick={() => setAuthMode('register')}
                  className={`rounded-full px-4 py-2 text-sm ${authMode === 'register' ? 'bg-amber-400 text-slate-900' : 'text-white'}`}
                >
                  Register
                </button>
              </div>
            </div>

            <form onSubmit={handleAuthSubmit} className="grid gap-4 md:grid-cols-2">
              {authMode === 'register' && (
                <label className="md:col-span-2 text-sm text-slate-300">
                  Full name
                  <input
                    value={authForm.full_name}
                    onChange={(e) => setAuthForm((prev) => ({ ...prev, full_name: e.target.value }))}
                    className="mt-2 w-full rounded-xl border border-white/10 bg-slate-950/60 px-4 py-3 text-white outline-none ring-0"
                    placeholder="Your full name"
                  />
                </label>
              )}

              <label className="md:col-span-2 text-sm text-slate-300">
                Email
                <input
                  type="email"
                  value={authForm.email}
                  onChange={(e) => setAuthForm((prev) => ({ ...prev, email: e.target.value }))}
                  className="mt-2 w-full rounded-xl border border-white/10 bg-slate-950/60 px-4 py-3 text-white outline-none ring-0"
                  placeholder="you@example.com"
                />
              </label>

              <label className="md:col-span-2 text-sm text-slate-300">
                Password
                <input
                  type="password"
                  value={authForm.password}
                  onChange={(e) => setAuthForm((prev) => ({ ...prev, password: e.target.value }))}
                  className="mt-2 w-full rounded-xl border border-white/10 bg-slate-950/60 px-4 py-3 text-white outline-none ring-0"
                  placeholder="At least 8 characters"
                />
              </label>

              <button
                type="submit"
                className="md:col-span-2 rounded-full bg-gradient-to-r from-amber-300 via-orange-400 to-yellow-500 px-6 py-3 font-semibold text-slate-950"
              >
                {authMode === 'register' ? 'Create account' : 'Sign in'}
              </button>
            </form>
          </section>
        )}

        <section className="flex flex-col gap-6 rounded-[32px] border border-white/10 bg-slate-900/60 p-6 backdrop-blur-xl">
          <div className="flex items-center justify-between">
            <h3 className="text-2xl font-bold">Top priority topics</h3>
            <button
              onClick={() => fileInputRef.current?.click()}
              className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-white/80"
            >
              {uploading ? 'Analyzing...' : 'Load My PDF'}
            </button>
          </div>

          <div className="grid gap-4 md:grid-cols-3">
            {topicEntries.map((topic) => (
              <div key={topic.topic} className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
                <div className="mb-2 flex items-center justify-between">
                  <span className="text-lg font-semibold text-white">{topic.topic}</span>
                  <span className="rounded-full bg-amber-400/10 px-2 py-1 text-xs font-medium text-amber-200">
                    Priority {Math.round(topic.priority)}
                  </span>
                </div>
                <p className="text-sm text-slate-300">Frequency: {topic.frequency}</p>
                <div className="mt-4 h-2 w-full rounded-full bg-slate-800">
                  <div
                    className="h-2 rounded-full bg-gradient-to-r from-amber-300 via-orange-400 to-yellow-500"
                    style={{ width: `${Math.round(topic.priority)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-10 flex flex-col gap-6 rounded-[32px] border border-white/10 bg-slate-900/60 p-6 backdrop-blur-xl">
          <div className="flex items-center justify-between">
            <h3 className="text-2xl font-bold">Topic Frequency & Priority</h3>
          </div>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={topicEntries} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                <XAxis dataKey="topic" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                <YAxis yAxisId="left" stroke="#fcd34d" tick={{ fill: '#fcd34d', fontSize: 12 }} />
                <YAxis yAxisId="right" orientation="right" stroke="#60a5fa" tick={{ fill: '#60a5fa', fontSize: 12 }} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                  itemStyle={{ color: '#e2e8f0' }}
                />
                <Legend wrapperStyle={{ paddingTop: '20px' }} />
                <Bar yAxisId="left" dataKey="priority" name="Priority Score" fill="#f59e0b" radius={[4, 4, 0, 0]} />
                <Bar yAxisId="right" dataKey="frequency" name="Frequency" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="mt-10 grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
          <div className="rounded-[32px] border border-white/10 bg-slate-900/60 p-6 backdrop-blur-xl">
            <div className="mb-5 flex items-center justify-between">
              <h3 className="text-2xl font-bold">Analysis summary</h3>
              <span className="rounded-full border border-cyan-400/20 bg-cyan-500/10 px-3 py-1 text-[10px] uppercase tracking-[0.22em] text-cyan-200">
                {analysis ? 'Live' : 'Demo'}
              </span>
            </div>
            <div className="grid gap-4 sm:grid-cols-3">
              <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
                <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Questions</div>
                <div className="mt-3 text-3xl font-black text-white">{analysis?.total_questions ?? 0}</div>
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
                <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Topics</div>
                <div className="mt-3 text-3xl font-black text-white">{analysis ? Object.keys(analysis.topics ?? {}).length : 0}</div>
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
                <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Focus</div>
                <div className="mt-3 text-lg font-black text-white">{analysis?.most_frequent_topic ?? 'N/A'}</div>
              </div>
            </div>
            <div className="mt-6 rounded-2xl border border-white/10 bg-slate-950/40 p-5">
              <div className="mb-3 flex items-center justify-between">
                <h4 className="text-lg font-semibold text-white">Question preview</h4>
                <span className="text-xs text-slate-400">From uploaded paper</span>
              </div>
              <ul className="space-y-3 text-sm text-slate-300">
                {(analysis?.questions ?? [
                  'Upload a PDF to see question preview.'
                ]).slice(0, 4).map((item, index) => (
                  <li key={index} className="rounded-xl border border-white/10 bg-white/[0.02] p-3">
                    {typeof item === 'string' ? item : item.question}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="rounded-[32px] border border-white/10 bg-gradient-to-br from-amber-400/10 via-slate-900/60 to-slate-900/60 p-6 backdrop-blur-xl">
            <div className="mb-5 flex items-center justify-between">
              <h3 className="text-2xl font-bold">Recommendation</h3>
              <span className="rounded-full border border-amber-400/20 bg-amber-500/10 px-3 py-1 text-[10px] uppercase tracking-[0.22em] text-amber-200">
                AI insight
              </span>
            </div>
            <div className="space-y-4 text-slate-200">
              <p className="text-lg leading-8">
                Your strongest opportunity is <span className="font-semibold text-white">{analysis?.most_frequent_topic ?? 'N/A'}</span>. It appears in the most frequent exam patterns and deserves the first study block.
              </p>
              <div className="rounded-2xl border border-white/10 bg-slate-950/40 p-4">
                <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Next best move</div>
                <p className="mt-2 text-base text-white">{analysis ? 'Revise the foundation concepts, then solve 3 targeted practice sets before the next revision cycle.' : 'Awaiting upload.'}</p>
              </div>
              <div className="rounded-2xl border border-white/10 bg-slate-950/40 p-4">
                <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Focus window</div>
                <p className="mt-2 text-base text-white">{plan?.study_window_days ?? 7} days of high-yield revision based on your last paper.</p>
              </div>
            </div>
          </div>
        </section>

        <section className="mt-10 flex flex-col gap-6 rounded-[32px] border border-white/10 bg-slate-900/60 p-6 backdrop-blur-xl">
          <div className="flex items-center justify-between">
            <h3 className="text-2xl font-bold">7-day study plan</h3>
            <span className="rounded-full border border-emerald-400/20 bg-emerald-500/10 px-3 py-1 text-xs uppercase tracking-[0.24em] text-emerald-200">
              {plan ? 'Generated' : 'Preview'}
            </span>
          </div>

          <div className="grid gap-4 lg:grid-cols-3">
            {planDays.map((day) => (
              <div key={day.day} className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
                <div className="mb-3 flex items-center justify-between">
                  <span className="text-sm uppercase tracking-[0.2em] text-slate-400">Day {day.day}</span>
                  <span className="text-xs font-medium text-amber-200">{day.duration_minutes} min</span>
                </div>
                <h4 className="text-xl font-semibold text-white">{day.topic}</h4>
                <div className="mt-4 space-y-2 text-sm text-slate-300">
                  <p>Learn:</p>
                  <ul className="list-disc space-y-1 pl-5">
                    {day.learn.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </div>
                <div className="mt-4 flex gap-4 text-xs uppercase tracking-[0.18em] text-slate-400">
                  <span>Practice {day.practice}</span>
                  <span>Quiz {day.quiz}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  )
}
