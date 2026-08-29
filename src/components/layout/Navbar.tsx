import { useState, useEffect } from 'react'
import { Link, NavLink, useLocation } from 'react-router-dom'
import { Menu, X } from 'lucide-react'
import Logo from './Logo'

const navItems = [
  { label: 'Home', path: '/' },
  { label: 'Crop Recommendation', path: '/crop-recommendation' },
  { label: 'Yield Prediction', path: '/yield-prediction' },
  { label: 'Farmer Advisory', path: '/farmer-advisory' },
  { label: 'Weather', path: '/weather-advisory' },
  { label: 'Dashboard', path: '/dashboard' },
]

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)
  const location = useLocation()

  useEffect(() => {
    setMobileOpen(false)
  }, [location.pathname])

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 10)
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <header
      className={`sticky top-0 z-50 transition-all duration-300 ${
        scrolled ? 'glass shadow-sm' : 'bg-transparent'
      }`}
    >
      <nav className="section-container flex h-16 items-center justify-between">
        <Link to="/" className="flex items-center gap-2 text-primary-700">
          <Logo />
          <span className="hidden font-display text-base font-bold sm:block">
            Smart Crop Advisory
          </span>
        </Link>

        {/* Desktop nav */}
        <div className="hidden items-center gap-1 lg:flex">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              className={({ isActive }) =>
                `rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-primary-50 text-primary-700'
                    : 'text-earth-600 hover:bg-earth-100 hover:text-earth-800'
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </div>

        {/* Mobile toggle */}
        <button
          onClick={() => setMobileOpen((v) => !v)}
          className="rounded-lg p-2 text-earth-700 transition-colors hover:bg-earth-100 lg:hidden"
          aria-label="Toggle menu"
        >
          {mobileOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </button>
      </nav>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="border-t border-earth-200 bg-white lg:hidden">
          <div className="section-container flex flex-col py-3">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.path === '/'}
                className={({ isActive }) =>
                  `rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-primary-50 text-primary-700'
                      : 'text-earth-600 hover:bg-earth-100'
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </div>
        </div>
      )}
    </header>
  )
}
