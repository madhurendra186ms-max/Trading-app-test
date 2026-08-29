import { useEffect, useState } from 'react'
import { Bell, ChevronDown, CircleAlert, RefreshCw, Search, SlidersHorizontal } from 'lucide-react'
import './App.css'
import './index-selector.css'

const gatewayUrl = import.meta.env.VITE_API_GATEWAY_URL ?? 'http://127.0.0.1:8009'
type Tick = { instrument: string; option_type: 'CE' | 'PE'; strike: number; bid: number; ask: number; ltp: number; oi: number; volume: number; iv: number }
type Row = { strike: number; call: Tick | null; put: Tick | null }
type Ranking = { instrument: string; option_type: 'CE' | 'PE'; score: number; spread_percent: number; ltp: number }
type Dashboard = { index: string; expiry: string; option_chain: { rows: Row[] }; rankings: { rankings: Ranking[] }; active_alert_rules: number }
type IndexVolume = { index: string; option_volume: number }
const sample: Dashboard = { index: 'NIFTY 50', expiry: '2026-09-04', option_chain: { rows: [{ strike: 24800, call: { instrument: 'NFO:NIFTY26SEP24800CE', option_type: 'CE', strike: 24800, bid: 132.45, ask: 133.2, ltp: 132.7, oi: 25000000, volume: 2170000, iv: 12.8 }, put: { instrument: 'NFO:NIFTY26SEP24800PE', option_type: 'PE', strike: 24800, bid: 97.85, ask: 98.4, ltp: 98.1, oi: 23500000, volume: 2050000, iv: 13.1 } }] }, rankings: { rankings: [{ instrument: 'NFO:NIFTY26SEP24800CE', option_type: 'CE', score: 94.37, spread_percent: 0.5631, ltp: 132.7 }, { instrument: 'NFO:NIFTY26SEP24800PE', option_type: 'PE', score: 93.5, spread_percent: 0.5589, ltp: 98.1 }] }, active_alert_rules: 1 }
const formatNumber = (value: number) => new Intl.NumberFormat('en-IN', { notation: 'compact', maximumFractionDigits: 1 }).format(value)

function App() {
  const [data, setData] = useState<Dashboard>(sample)
  const [selected, setSelected] = useState<Tick>(sample.option_chain.rows[0].call!)
  const [loading, setLoading] = useState(true)
  const [isLive, setIsLive] = useState(false)
  const [error, setError] = useState('')
  const [selectedIndex, setSelectedIndex] = useState('NIFTY 50')
  const [topIndexes, setTopIndexes] = useState<IndexVolume[]>([{ index: 'NIFTY 50', option_volume: 0 }])

  const loadDashboard = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${gatewayUrl}/v1/dashboard?index=${encodeURIComponent(selectedIndex)}&expiry=2026-09-04`)
      if (!response.ok) throw new Error('Gateway unavailable')
      const liveData: Dashboard = await response.json()
      setData(liveData)
      const first = liveData.option_chain.rows.flatMap((row) => [row.call, row.put]).find(Boolean)
      if (first) setSelected(first)
      setIsLive(true)
      setError('')
    } catch {
      setData(sample)
      setSelected(sample.option_chain.rows[0].call!)
      setIsLive(false)
      setError('Showing sample data while API Gateway is unavailable.')
    } finally { setLoading(false) }
  }

  useEffect(() => { void loadDashboard() }, [selectedIndex])
  useEffect(() => {
    const loadIndexes = async () => {
      try {
        const response = await fetch(`${gatewayUrl}/v1/indexes/top-volume`)
        if (!response.ok) throw new Error('Index list unavailable')
        const indexes: IndexVolume[] = await response.json()
        if (indexes.length) setTopIndexes(indexes)
      } catch { }
    }
    void loadIndexes()
  }, [])
  const ranking = data.rankings.rankings.find((item) => item.instrument === selected.instrument)
  const premium = selected.ask
  const breakeven = selected.option_type === 'CE' ? selected.strike + premium : selected.strike - premium

  return (
    <main className="desk-shell">
      <header className="topbar"><div className="brand"><span className="brand-mark">N</span><div><strong>NORTHSTAR</strong><span>OPTIONS DESK</span></div></div><nav><button className="nav-active">Market desk</button><button>Watchlist</button><button>Alerts <b>{data.active_alert_rules}</b></button></nav><div className="status"><span className={isLive ? 'dot live' : 'dot'}></span>{isLive ? 'Live feed' : 'Sample feed'}<button className="icon-button" onClick={() => void loadDashboard()} title="Refresh market data"><RefreshCw size={16} className={loading ? 'spin' : ''} /></button></div></header>
      <section className="market-strip"><div className="market-title"><p>Underlying</p><h1>{data.index} <ChevronDown size={17} /></h1></div><div className="quote"><p>Spot reference</p><strong>24,820.40</strong><span className="up">+0.42%</span></div><div className="quote"><p>Selected expiry</p><strong>{data.expiry}</strong><span>Thursday</span></div><div className="quote"><p>Active alerts</p><strong>{data.active_alert_rules}</strong><span>Session only</span></div><div className="market-actions"><button className="icon-button" title="Search contracts"><Search size={18} /></button><button className="icon-button" title="Chain filters"><SlidersHorizontal size={18} /></button><button className="icon-button" title="Alert center"><Bell size={18} /></button></div></section>
      <section className="index-selector" aria-label="Top option-volume indexes"><label htmlFor="index-select">Top volume today</label><select id="index-select" value={selectedIndex} onChange={(event) => setSelectedIndex(event.target.value)}>{topIndexes.map((item) => <option key={item.index} value={item.index}>{item.index} · {formatNumber(item.option_volume)} options</option>)}</select></section>
      {error && <div className="notice"><CircleAlert size={16} />{error}</div>}
      <div className="workspace"><section className="chain-panel panel"><div className="panel-heading"><div><p className="eyebrow">Live option chain</p><h2>Expiry {data.expiry}</h2></div><span className="pill">ATM nearby</span></div><div className="chain-scroll"><table><thead><tr><th colSpan={4} className="call-head">CALLS</th><th>STRIKE</th><th colSpan={4} className="put-head">PUTS</th></tr><tr className="subhead"><th>OI</th><th>Vol.</th><th>Bid</th><th>Ask</th><th></th><th>Bid</th><th>Ask</th><th>Vol.</th><th>OI</th></tr></thead><tbody>{data.option_chain.rows.map((row) => <tr key={row.strike} className={row.strike === 24800 ? 'atm' : ''}><td>{row.call ? formatNumber(row.call.oi) : '—'}</td><td>{row.call ? formatNumber(row.call.volume) : '—'}</td><td><button className="quote-button call" onClick={() => row.call && setSelected(row.call)} disabled={!row.call}>{row.call?.bid.toFixed(2) ?? '—'}</button></td><td><button className="quote-button call" onClick={() => row.call && setSelected(row.call)} disabled={!row.call}>{row.call?.ask.toFixed(2) ?? '—'}</button></td><td className="strike">{row.strike.toLocaleString('en-IN')} {row.strike === 24800 && <span>ATM</span>}</td><td><button className="quote-button put" onClick={() => row.put && setSelected(row.put)} disabled={!row.put}>{row.put?.bid.toFixed(2) ?? '—'}</button></td><td><button className="quote-button put" onClick={() => row.put && setSelected(row.put)} disabled={!row.put}>{row.put?.ask.toFixed(2) ?? '—'}</button></td><td>{row.put ? formatNumber(row.put.volume) : '—'}</td><td>{row.put ? formatNumber(row.put.oi) : '—'}</td></tr>)}</tbody></table></div><footer className="chain-footer"><span>Click any bid or ask to inspect a contract.</span><button className="text-button">Expand chain</button></footer></section>
      <aside className="trade-panel panel"><div className="panel-heading"><div><p className="eyebrow">Selected contract</p><h2>{selected.strike.toLocaleString('en-IN')} {selected.option_type}</h2></div><span className={selected.option_type === 'CE' ? 'side call-tag' : 'side put-tag'}>{selected.option_type === 'CE' ? 'CALL' : 'PUT'}</span></div><p className="instrument">{selected.instrument}</p><div className="price-grid"><div><span>Bid</span><strong>{selected.bid.toFixed(2)}</strong></div><div><span>Ask</span><strong>{selected.ask.toFixed(2)}</strong></div><div><span>LTP</span><strong>{selected.ltp.toFixed(2)}</strong></div></div><div className="metric"><span>Liquidity score</span><strong>{ranking?.score.toFixed(2) ?? '—'} <small>/ 100</small></strong></div><div className="metric"><span>Bid-ask spread</span><strong>{ranking?.spread_percent.toFixed(2) ?? '—'}<small>%</small></strong></div><div className="risk-box"><p>Long option estimate</p><div><span>Breakeven</span><strong>{breakeven.toFixed(2)}</strong></div><div><span>Maximum premium risk</span><strong>{premium.toFixed(2)} pts</strong></div><div><span>Lot size / charges</span><strong>Not connected</strong></div></div><button className="prepare-button" type="button">Prepare trade <span>→</span></button><p className="disclaimer">Estimate only. No order is submitted from this dashboard.</p></aside></div>
    </main>
  )
}

export default App
