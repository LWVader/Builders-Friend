'use client'

import { useState } from 'react'
import { processComplianceCheck } from './actions'

export default function ComplianceDashboard() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    
    const formData = new FormData(e.currentTarget)
    const res = await processComplianceCheck(formData)
    
    setLoading(false)
    if (res.error) {
      setError(res.error)
      setResult(null)
    } else {
      setResult(res)
    }
  }

  return (
    <main className="min-h-screen bg-slate-900 text-slate-100 flex flex-col md:flex-row">
      
      {/* LEFT SIDEBAR PANEL: Controls & Map Placeholder */}
      <div className="w-full md:w-1/3 p-6 border-r border-slate-800 bg-slate-950 flex flex-col justify-between">
        <div>
          <div className="flex items-center space-x-2 mb-6">
            <span className="text-2xl">👷‍♂️</span>
            <h1 className="text-xl font-bold tracking-tight bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
              Builders Friend AI
            </h1>
          </div>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Louisville Property Address
              </label>
              <input
                name="address"
                type="text"
                required
                placeholder="e.g., 1234 Bardstown Rd"
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:border-blue-500 transition-colors placeholder:text-slate-500 text-sm"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Compliance Inquiry
              </label>
              <textarea
                name="question"
                required
                rows={3}
                placeholder="What are the building height limitations or maximum setback regulations?"
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:border-blue-500 transition-colors placeholder:text-slate-500 text-sm resize-none"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-emerald-600 hover:from-blue-500 hover:to-emerald-500 text-white font-medium rounded-lg py-2.5 text-sm transition-all focus:outline-none disabled:opacity-50"
            >
              {loading ? 'Analyzing Regulations...' : 'Run Compliance Scan'}
            </button>
          </form>

          {error && (
            <div className="mt-4 p-3 bg-red-950/50 border border-red-800 text-red-200 text-xs rounded-lg">
              {error}
            </div>
          )}
        </div>

        {/* Dynamic Map Placement Wrapper */}
        <div className="mt-6 h-48 bg-slate-900 border border-slate-800 rounded-xl flex flex-col items-center justify-center text-center p-4 relative overflow-hidden">
          <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#3b82f6_1px,transparent_1px)] [background-size:16px_16px]"></div>
          <span className="text-2xl mb-1">🗺️</span>
          <p className="text-xs font-medium text-slate-300">Spatial Map Engine Active</p>
          {result?.parcel && (
            <p className="text-[10px] text-blue-400 font-mono mt-1">
              Loaded: {result.parcel.zoningCode} Polygon Grid
            </p>
          )}
        </div>
      </div>

      {/* RIGHT MAIN PANEL: Live Digital Twin Assessment Results */}
      <div className="flex-1 p-6 lg:p-10 flex flex-col justify-start overflow-y-auto">
        {!result ? (
          <div className="h-full flex flex-col items-center justify-center text-slate-500 max-w-md mx-auto text-center">
            <span className="text-4xl mb-3">🏢</span>
            <p className="text-sm font-medium">Ready for Query Initialization</p>
            <p className="text-xs text-slate-600 mt-1">
              Submit a target site address along with zoning compliance questions to retrieve legal land code assessments instantly.
            </p>
          </div>
        ) : (
          <div className="space-y-6 max-w-4xl">
            {/* SITE IDENTIFICATION TRAITS */}
            <div className="bg-slate-950 border border-slate-800 rounded-xl p-5 shadow-sm">
              <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-1">Verified Location Details</h2>
              <p className="text-lg font-semibold text-white mb-4">{result.parcel.formattedAddress}</p>
              
              <div className="flex flex-wrap gap-3">
                <div className="bg-blue-950/60 border border-blue-800/60 rounded-lg px-3 py-1.5 flex items-center space-x-2">
                  <span className="w-2 h-2 rounded-full bg-blue-400"></span>
                  <span className="text-xs font-medium text-blue-300">Zoning Designation: {result.parcel.zoningCode}</span>
                </div>
                <div className="bg-emerald-950/60 border border-emerald-800/60 rounded-lg px-3 py-1.5 flex items-center space-x-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                  <span className="text-xs font-medium text-emerald-300">Form District: {result.parcel.formDistrict}</span>
                </div>
              </div>
            </div>

            {/* DYNAMIC RETRIEVED CITATIONS LIST */}
            <div className="space-y-4">
              <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Matched Legal Code Citations</h3>
              
              {result.citations.length === 0 ? (
                <p className="text-xs text-slate-500 italic">No structured matches resolved inside current land documentation vectors.</p>
              ) : (
                result.citations.map((doc: any, index: number) => (
                  <div key={index} className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition-all">
                    <div className="flex justify-between items-center mb-3">
                      <span className="text-xs font-bold text-slate-400 font-mono">CITATION 0{index + 1}</span>
                      <span className="text-[11px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded-md font-mono">
                        Match Score: {(doc.similarity * 100).toFixed(1)}%
                      </span>
                    </div>
                    <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap mb-4">
                      {doc.content}
                    </p>
                    {doc.metadata && (
                      <div className="border-t border-slate-800/80 pt-3 flex flex-wrap gap-4 text-[11px] font-mono text-slate-500">
                        <div><span className="text-slate-400">ID:</span> {doc.id}</div>
                        <div><span className="text-slate-400">Type:</span> Zoning Regulatory Text</div>
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          </div>
        )}
      </div>
    </main>
  )
}