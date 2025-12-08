import React from 'react';

/**
 * CareerLens Logo Component
 * "Focus Aperture" design - A stylized camera aperture forming a "C" shape
 * Represents clarity, focus, and AI "zooming in" on the right opportunities
 */

interface LogoProps {
  variant?: 'full' | 'icon' | 'text';
  size?: 'sm' | 'default' | 'lg' | 'xl';
  className?: string;
  darkMode?: boolean;
}

const Logo: React.FC<LogoProps> = ({ 
  variant = 'full',
  size = 'default',
  className = '',
  darkMode = false 
}) => {
  const sizeClasses = {
    sm: { icon: 'w-6 h-6', text: 'text-lg', container: 'gap-2' },
    default: { icon: 'w-8 h-8', text: 'text-xl', container: 'gap-2' },
    lg: { icon: 'w-12 h-12', text: 'text-2xl', container: 'gap-3' },
    xl: { icon: 'w-16 h-16', text: 'text-3xl', container: 'gap-4' },
  };

  const currentSize = sizeClasses[size] || sizeClasses.default;

  const ApertureIcon: React.FC = () => {
    const accentColor = darkMode ? '#60A5FA' : '#3B82F6';
    const centerColor = darkMode ? '#1F2937' : '#1A2B45';
    
    return (
      <svg 
        className={currentSize.icon}
        viewBox="0 0 100 100" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
        aria-label="CareerLens Logo"
      >
        {/* Outer circle for depth */}
        <circle 
          cx="50" 
          cy="50" 
          r="45" 
          stroke={accentColor} 
          strokeWidth="10" 
          className="opacity-20"
        />
        
        {/* The Aperture Blades forming a C shape */}
        <path 
          d="M50 25L65 50L50 75L35 50L50 25Z" 
          fill={accentColor}
        />
        
        {/* C-shaped arc */}
        <path 
          d="M85 50C85 69.33 69.33 85 50 85C30.67 85 15 69.33 15 50" 
          stroke={accentColor} 
          strokeWidth="10" 
          strokeLinecap="round"
        />
        
        {/* Center focus point */}
        <circle 
          cx="50" 
          cy="50" 
          r="8" 
          fill={centerColor}
        />
      </svg>
    );
  };

  if (variant === 'icon') {
    return (
      <div className={`inline-flex items-center ${className}`}>
        <ApertureIcon />
      </div>
    );
  }

  if (variant === 'text') {
    return (
      <div className={`inline-flex items-center ${currentSize.container} ${className}`}>
        <span className={`font-bold ${currentSize.text} text-text-heading dark:text-dark-text-primary`}>
          CareerLens
        </span>
      </div>
    );
  }

  // Full logo (icon + text)
  return (
    <div className={`inline-flex items-center ${currentSize.container} ${className}`}>
      <ApertureIcon />
      <span className={`font-bold ${currentSize.text} text-text-heading dark:text-dark-text-primary`}>
        CareerLens
      </span>
    </div>
  );
};

export default Logo;
