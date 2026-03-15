import { type FC } from 'react';
import type { HistoryItem } from '@/types/history';
import { HistoryTimelineItem } from './HistoryTimelineItem';
import { EmptyState } from '@/components/common/EmptyState';

interface HistoryTimelineProps {
  items: HistoryItem[];
}

export const HistoryTimeline: FC<HistoryTimelineProps> = ({ items }) => {
  if (items.length === 0) {
    return <EmptyState message="Nenhum evento de histórico encontrado nos filtros atuais." />;
  }

  return (
    <div className="max-w-4xl mx-auto py-4 pl-4 md:pl-0">
       <div className="space-y-0">
          {items.map((item, index) => {
            const key = item.message_id || `${item.local_id}-${item.timestamp}-${index}`;
            return <HistoryTimelineItem key={key} item={item} />;
          })}
       </div>
    </div>
  );
};
