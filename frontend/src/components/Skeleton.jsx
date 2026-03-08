// src/components/Skeleton.jsx
import React from "react";

/** Single shimmer line */
export const SkeletonLine = ({ width = "100%", height = 14, style }) => (
    <div
        className="skeleton skeleton-line"
        style={{ width, height, ...style }}
    />
);

/** Card-shaped skeleton (for news grid) */
export const SkeletonCard = () => (
    <div className="skeleton-card">
        <SkeletonLine width="35%" height={10} />
        <div style={{ height: 8 }} />
        <SkeletonLine width="90%" height={16} />
        <SkeletonLine width="70%" height={16} />
        <div style={{ height: 6 }} />
        <SkeletonLine width="100%" height={12} />
        <SkeletonLine width="85%" height={12} />
        <SkeletonLine width="60%" height={12} />
    </div>
);

/** Table-row skeleton (for market / sentiment tables) */
export const SkeletonTable = ({ rows = 6, cols = 5 }) => (
    <div>
        {Array.from({ length: rows }).map((_, i) => (
            <div className="skeleton-table-row" key={i}>
                {Array.from({ length: cols }).map((_, j) => (
                    <div className="skeleton skeleton-cell" key={j} />
                ))}
            </div>
        ))}
    </div>
);

/** News grid skeleton */
export const SkeletonNewsGrid = ({ count = 6 }) => (
    <div className="news-grid">
        {Array.from({ length: count }).map((_, i) => (
            <SkeletonCard key={i} />
        ))}
    </div>
);

const SkeletonComponents = { SkeletonLine, SkeletonCard, SkeletonTable, SkeletonNewsGrid };
export default SkeletonComponents;
