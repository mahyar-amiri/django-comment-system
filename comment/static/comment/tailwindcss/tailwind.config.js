// /* @type {import('tailwindcss').Config} */
tailwind.config = {
    darkMode: ['class', '[data-mode="dark"]'],
    content: [
        '../../templates/**/*.html',
        '../js/**/*.js'
    ],
    theme: {
        fontFamily: {
            'default': ['Vazirmatn', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'Noto Sans', 'sans-serif', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'],
            'default-fd': ['Vazirmatn FD', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'Noto Sans', 'sans-serif', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji']
        },
        extend: {

            colors: {
                // LIGHT
                'text-light': '#ffffff',
                'background-light': '#f8fafc',
                // TEXTAREA
                'textarea-bg-light': '#e5e7eb',
                'textarea-scroll-light': '#9ca3af',
                'textarea-text-light': '#000000',
                'textarea-text-selection-light': '#c7d2fe',
                'textarea-text-placeholder-light': '#6b7280',
                'textarea-border-empty-light': '#f87171',
                // ICON
                'icon-spoiler-light': '#6b7280',
                'icon-spoiler-option-light': '#111827',
                'icon-dots-light': '#6b7280',
                'icon-pin-light': '#6b7280',
                'icon-edit-light': '#16a34a',
                'icon-delete-light': '#ef4444',
                'icon-pagination-light': '#9ca3af',
                'icon-pagination-hover-light': '#374151',
                // BUTTON
                'btn-send-bg-light': '#000000',
                'btn-send-text-light': '#ffffff',
                'btn-edit-bg-light': '#16a34a',
                'btn-edit-text-light': '#ffffff',
                'btn-reply-bg-light': '#2563eb',
                'btn-reply-text-light': '#ffffff',
                'btn-delete-bg-light': '#dc2626',
                'btn-delete-text-light': '#ffffff',
                'btn-cancel-bg-light': '#6b7280',
                'btn-cancel-text-light': '#ffffff',
                'btn-login-text-light': '#1d4ed8',
                // DELETE FORM
                'delete-from-bg-light': '#ffffff',
                'delete-from-text-light': '#111827',
                'delete-from-subtext-light': '#6b7280',
                // COUNTER
                'section-primary-light': '#e5e7eb',
                'section-secondary-light': '#000000',
                'section-text-light': '#000000',
                'section-number-bg-light': '#e5e7eb',
                'section-number-text-light': '#000000',
                // PAGINATION
                'page-current-bg-light': '#000000',
                'page-current-text-light': '#ffffff',
                'page-bg-light': 'transparent',
                'page-bg-hover-light': '#9ca3af',
                'page-text-light': '#9ca3af',
                'page-text-hover-light': '#ffffff',
                // COMMENT
                'comment-parent-bg-light': '#f8fafc',
                'comment-parent-border-light': '#e5e7eb',
                'comment-child-bg-light': '#f8fafc',
                'comment-child-border-light': '#a5b4fc',
                // REPLY
                'reply-text-light': '#1d4ed8',
                'reply-border-light': '#4b5563',
                // REACTION
                'react-default-bg-light': '#f3f4f6',
                'react-default-border-light': '#e5e7eb',
                'react-selected-bg-light': '#dbeafe',
                'react-selected-border-light': '#bfdbfe',
                'react-count-text-light': '#000000',
                // COMMENT BODY
                'comment-name-text-light': '#000000',
                'comment-time-text-light': '#6b7280',
                'comment-option-bg-light': '#f3f4f6',
                'comment-option-borer-light': '#6b7280',
                'comment-read-more-light': '#1d4ed8',

                // DARK
                'text-dark': '#000000',
                'background-dark': '#1e293b',
                // TEXTAREA
                'textarea-bg-dark': '#475569',
                'textarea-scroll-dark': '#9ca3af',
                'textarea-text-dark': '#f3f4f6',
                'textarea-text-selection-dark': '#4338ca',
                'textarea-text-placeholder-dark': '#94a3b8',
                'textarea-border-empty-dark': '#f87171',
                // ICON
                'icon-spoiler-dark': '#e5e7eb',
                'icon-spoiler-option-dark': '#e5e7eb',
                'icon-dots-dark': '#e5e7eb',
                'icon-pin-dark': '#d1d5db',
                'icon-edit-dark': '#4ade80',
                'icon-delete-dark': '#f87171',
                'icon-pagination-dark': '#9ca3af',
                'icon-pagination-hover-dark': '#6b7280',
                // BUTTON
                'btn-send-bg-dark': '#e2e8f0',
                'btn-send-text-dark': '#000000',
                'btn-edit-bg-dark': '#16a34a',
                'btn-edit-text-dark': '#ffffff',
                'btn-reply-bg-dark': '#2563eb',
                'btn-reply-text-dark': '#ffffff',
                'btn-delete-bg-dark': '#ef4444',
                'btn-delete-text-dark': '#ffffff',
                'btn-cancel-bg-dark': '#e2e8f0',
                'btn-cancel-text-dark': '#000000',
                'btn-login-text-dark': '#60a5fa',
                // COUNTER
                'section-primary-dark': '#374151',
                'section-secondary-dark': '#e5e7eb',
                'section-text-dark': '#ffffff',
                'section-number-bg-dark': '#4b5563',
                'section-number-text-dark': '#000000',
                // DELETE FORM
                'delete-from-bg-dark': '#475569',
                'delete-from-text-dark': '#f3f4f6',
                'delete-from-subtext-dark': '#d1d5db',
                // PAGINATION
                'page-current-bg-dark': '#475569',
                'page-current-text-dark': '#ffffff',
                'page-bg-dark': 'transparent',
                'page-bg-hover-dark': '#334155',
                'page-text-dark': '#9ca3af',
                'page-text-hover-dark': '#ffffff',
                // COMMENT
                'comment-parent-bg-dark': '#1e293b',
                'comment-parent-border-dark': '#4b5563',
                'comment-child-bg-dark': '#1e293b',
                'comment-child-border-dark': '#a5b4fc',
                // REPLY
                'reply-text-dark': '#93c5fd',
                'reply-border-dark': '#4b5563',
                // REACTION
                'react-default-bg-dark': '#334155',
                'react-default-border-dark': '#6b7280',
                'react-selected-bg-dark': '#64748b',
                'react-selected-border-dark': '#1e293b',
                'react-count-text-dark': '#f3f4f6',
                // COMMENT BODY
                'comment-name-text-dark': '#f3f4f6',
                'comment-time-text-dark': '#d1d5db',
                'comment-option-bg-dark': '#475569',
                'comment-option-borer-dark': '#6b7280',
                'comment-read-more-dark': '#93c5fd',
            },
            backgroundImage: ['hover', 'group-hover']
        },
    },
    plugins: [],
}
