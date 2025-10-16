# YikYak Clone for South Lake Union - Project Plan

## Goal
Build a location-based anonymous social app for Amazon employees in South Lake Union, Seattle. Users can post anonymous messages (yaks), upvote/downvote posts, comment, and see posts from nearby users.

---

## Phase 1: Core Feed and Post Creation ✅
- [x] Design main feed layout with Material Design 3 (teal primary, gray secondary, Poppins font)
- [x] Create post/yak card components with elevation, vote counts, time stamps
- [x] Implement anonymous post creation with character limit (200 chars)
- [x] Add upvote/downvote functionality with vote count display
- [x] Build state management for posts (create, vote, display)
- [x] Add mock location filter for South Lake Union area

---

## Phase 2: Comments and Interactions ✅
- [x] Implement comment system for each yak
- [x] Add comment thread view with nested replies
- [x] Create comment creation form with character limit (150 chars)
- [x] Implement post detail view showing all comments
- [x] Add "Hot" and "Recent" feed sorting options
- [x] Add back navigation from post detail to main feed

---

## Phase 3: User Experience and Polish ✅
- [x] Add floating action button (FAB) for quick post creation
- [x] Implement real-time post updates and animations with Material transitions
- [x] Add peek score system (user reputation based on upvotes)
- [x] Create notifications for replies and popular posts using rx.toast
- [x] Add report/flag functionality for inappropriate content
- [x] Implement post deletion (by author) with peek score penalty
- [x] Polish UI with Material motion, ripple effects, and transitions
- [x] Add dropdown menu on posts with report and delete options
- [x] Add proper shadow elevation for cards and buttons
- [x] Implement sticky header with backdrop blur

---

## Completed Features

### Core Functionality
- Anonymous posting with 200 character limit
- Upvote/downvote system with vote tracking
- Comment system with 150 character limit
- Post detail view with comment thread
- Hot and New sorting algorithms

### User Experience
- Peek Score reputation system (starts at 137)
  - +10 for creating a post
  - +1 for receiving an upvote
  - -1 for receiving a downvote
  - -10 for deleting a post
- Toast notifications for all actions
- Floating Action Button (FAB) for quick posting
- Dropdown menu on each post (report/delete)
- Post ownership tracking for delete permission

### Design
- Material Design 3 principles
- Teal primary color (#14b8a6)
- Gray secondary color scheme
- Poppins font family
- Proper elevation shadows (1dp, 4dp, 8dp)
- Smooth transitions and hover effects
- Backdrop blur on sticky header
- Rounded corners (8px, 12px, 16px)

### Navigation
- Main feed at "/"
- Post detail page at "/post/[post_id]"
- Back navigation to feed
- Click on post card to view details

---

## Notes
- Using Material Design 3 with teal primary color and gray secondary
- Font: Poppins
- Anonymous posting - no user accounts initially
- Focus on Amazon employee community in South Lake Union
- Character limits: Posts (200 chars), Comments (150 chars)
- All three phases completed successfully!