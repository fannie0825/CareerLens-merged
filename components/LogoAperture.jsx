/**
 * CareerLens Logo Component - Focus Aperture Design
 * A stylized camera aperture forming a "C" shape
 * Represents clarity, focus, and AI "zooming in" on the right opportunities
 */

export const LogoAperture = ({ className = "w-8 h-8", darkMode = false }) => {
  const accentColor = darkMode ? '#60A5FA' : '#3B82F6';
  const centerColor = darkMode ? '#1F2937' : '#1A2B45';
  
  return (
    <svg 
      viewBox="0 0 100 100" 
      className={className} 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      aria-label="CareerLens Logo"
    >
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
      <path 
        d="M85 50C85 69.33 69.33 85 50 85C30.67 85 15 69.33 15 50" 
        stroke={accentColor} 
        strokeWidth="10" 
        strokeLinecap="round" 
      />
      <circle 
        cx="50" 
        cy="50" 
        r="8" 
        fill={centerColor} 
      />
    </svg>
  );
};
