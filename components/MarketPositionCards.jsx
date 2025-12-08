import React from 'react';
import { TrendingUp, AlertCircle, Award } from 'lucide-react';
import LoadingSpinner from './LoadingSpinner';

const MarketPositionCards = ({ data = null, loading = false }) => {
  const defaultCards = [
    {
      id: 1,
      title: 'Estimated Salary Band',
      value: 'HK$45k-60k',
      icon: TrendingUp,
      iconColor: 'text-status-success',
      iconBg: 'bg-status-success/10',
      delta: '+12% vs market avg',
      deltaColor: 'text-status-success',
      description: 'Your experience aligns with mid-senior level roles'
    },
    {
      id: 2,
      title: 'Top Skill Gap',
      value: 'Cloud Architecture',
      icon: AlertCircle,
      iconColor: 'text-status-warning',
      iconBg: 'bg-status-warning/10',
      delta: 'High demand in HK',
      deltaColor: 'text-status-warning',
      description: 'Consider AWS or Azure certifications'
    },
    {
      id: 3,
      title: 'Recommended Accreditation',
      value: 'AWS Certified Solutions Architect',
      icon: Award,
      iconColor: 'text-accent',
      iconBg: 'bg-accent/10',
      delta: 'Unlock 15% more roles',
      deltaColor: 'text-accent',
      description: 'Most valued certification in your target market'
    }
  ];

  // Use provided data or fallback to default mock data
  const cards = data ? [
    {
      id: 1,
      title: 'Estimated Salary Band',
      value: data.salaryBand || 'HK$45k-60k',
      icon: TrendingUp,
      iconColor: 'text-status-success',
      iconBg: 'bg-status-success/10',
      delta: data.salaryDelta || '+12% vs market avg',
      deltaColor: 'text-status-success',
      description: data.salaryDescription || 'Your experience aligns with mid-senior level roles'
    },
    {
      id: 2,
      title: 'Top Skill Gap',
      value: data.topSkillGap || 'Cloud Architecture',
      icon: AlertCircle,
      iconColor: 'text-status-warning',
      iconBg: 'bg-status-warning/10',
      delta: data.skillGapDelta || 'High demand in HK',
      deltaColor: 'text-status-warning',
      description: data.skillGapDescription || 'Consider AWS or Azure certifications'
    },
    {
      id: 3,
      title: 'Recommended Accreditation',
      value: data.recommendedAccreditation || 'AWS Certified Solutions Architect',
      icon: Award,
      iconColor: 'text-accent',
      iconBg: 'bg-accent/10',
      delta: data.accreditationDelta || 'Unlock 15% more roles',
      deltaColor: 'text-accent',
      description: data.accreditationDescription || 'Most valued certification in your target market'
    }
  ] : defaultCards;

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {[1, 2, 3].map((i) => (
          <div key={i} className="card p-6 bg-bg-card dark:bg-dark-bg-card border-card">
            <div className="flex items-center justify-center py-8">
              <LoadingSpinner size="lg" />
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      {cards.map((card) => {
        const Icon = card.icon;
        return (
          <div
            key={card.id}
            className="card card-hover p-6 bg-bg-card dark:bg-dark-bg-card border-card"
          >
            <div className="flex items-start justify-between mb-4">
              <div className={`${card.iconBg} p-3 rounded-lg`}>
                <Icon className={`w-6 h-6 ${card.iconColor}`} />
              </div>
            </div>
            
            <h3 className="text-sm font-semibold text-text-muted dark:text-dark-text-secondary mb-2 uppercase tracking-wide">
              {card.title}
            </h3>
            
            <p className="text-2xl font-bold text-text-heading dark:text-dark-text-primary mb-2">
              {card.value}
            </p>
            
            <p className={`text-sm font-medium ${card.deltaColor} mb-1`}>
              {card.delta}
            </p>
            
            <p className="text-xs text-text-muted dark:text-dark-text-secondary mt-2">
              {card.description}
            </p>
          </div>
        );
      })}
    </div>
  );
};

export default MarketPositionCards;
