"use client";

import { MainFooter, NavbarLanding, VideoHeroLanding, VideoThumbnail } from "@/components";
import { AnimatePresence, motion } from "framer-motion";
import { ArrowRight, Play, Plus, Users } from "lucide-react";
import Head from "next/head";
import Link from "next/link";
import { useState } from "react";

/**
 * Video Landing Page - BNSCLIENT1.md Aligned
 * 
 * Features:
 * - Full-screen video hero
 * - Category-based navigation (Basics | Finance Bill | National | County | Sector | Tracker Stories)
 * - Video grid with filtering
 * - CTA Strip: Request a Topic | Join Training
 * - Focused content on videos
 */

type VideoCategory = "all" | "basics" | "finance-bill" | "national" | "county" | "sector" | "tracker-stories";

interface VideoItem {
  id: number;
  title: string;
  description: string;
  duration: string;
  thumbnail?: string;
  videoUrl: string;
  category: VideoCategory;
  date: string;
}

// Sample video data - in production this would come from API/CMS
const sampleVideos: VideoItem[] = [
  {
    id: 1,
    title: "Understanding the National Budget",
    description: "A beginner's guide to Kenya's national budget process and key terms.",
    duration: "5:30",
    videoUrl: "https://youtu.be/example1",
    category: "basics",
    date: "2026-01-15",
  },
  {
    id: 2,
    title: "Finance Bill 2026 Explained",
    description: "What the new Finance Bill means for ordinary Kenyans.",
    duration: "8:45",
    videoUrl: "https://youtu.be/example2",
    category: "finance-bill",
    date: "2026-02-01",
  },
  {
    id: 3,
    title: "Health Budget Breakdown",
    description: "Where the money goes in Kenya's healthcare sector.",
    duration: "12:20",
    videoUrl: "https://youtu.be/example3",
    category: "national",
    date: "2026-01-20",
  },
  {
    id: 4,
    title: "Nairobi County Budget Overview",
    description: "Understanding how Nairobi allocates its development funds.",
    duration: "10:15",
    videoUrl: "https://youtu.be/example4",
    category: "county",
    date: "2026-01-25",
  },
  {
    id: 5,
    title: "Education Sector Analysis",
    description: "Deep dive into education funding and what's changing.",
    duration: "15:00",
    videoUrl: "https://youtu.be/example5",
    category: "sector",
    date: "2026-02-05",
  },
  {
    id: 6,
    title: "Tracking Road Projects in Kiambu",
    description: "Following the money from budget to completed roads.",
    duration: "7:30",
    videoUrl: "https://youtu.be/example6",
    category: "tracker-stories",
    date: "2026-02-10",
  },
];

const categories: { id: VideoCategory; label: string }[] = [
  { id: "all", label: "All Videos" },
  { id: "basics", label: "Basics" },
  { id: "finance-bill", label: "Finance Bill" },
  { id: "national", label: "National" },
  { id: "county", label: "County" },
  { id: "sector", label: "Sector" },
  { id: "tracker-stories", label: "Tracker Stories" },
];

export default function VideoLanding() {
  const [activeCategory, setActiveCategory] = useState<VideoCategory>("all");

  const filteredVideos = activeCategory === "all" 
    ? sampleVideos 
    : sampleVideos.filter(v => v.category === activeCategory);

  return (
    <>
      <Head>
        <title>Videos — Budget Ndio Story</title>
        <meta
          name="description"
          content="Short explainers made for mobile. Watch budget breakdowns, county analysis, and tracker stories."
        />
        <meta property="og:title" content="Videos — Budget Ndio Story" />
        <meta
          property="og:description"
          content="Short explainers made for mobile. Watch budget breakdowns and tracker stories."
        />
        <meta name="theme-color" content="#0a0a0a" />
      </Head>

      <div className="bg-[#0a0a0a] text-white min-h-screen">
        {/* Navigation */}
        <NavbarLanding />

        {/* Video Hero */}
        <VideoHeroLanding />

        <main>
          {/* CATEGORY NAVIGATION */}
          <section className="padding-x pt-12 pb-6">
            <div className="max-w-6xl mx-auto">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5 }}
                className="text-center mb-8"
              >
                <h2 className="font-neue-montreal text-2xl lg:text-3xl font-semibold">
                  Browse by Category
                </h2>
              </motion.div>

              {/* Category Tabs - Horizontal scroll on mobile */}
              <div className="overflow-x-auto pb-4 -mx-4 px-4 scrollbar-hide">
                <div className="flex gap-2 min-w-max">
                  {categories.map((cat) => (
                    <button
                      key={cat.id}
                      onClick={() => setActiveCategory(cat.id)}
                      className={`px-5 py-2.5 rounded-full text-sm font-NeueMontreal uppercase tracking-wider transition-all duration-300 whitespace-nowrap ${
                        activeCategory === cat.id
                          ? "bg-[#00aa55] text-black"
                          : "bg-white/10 text-white/70 hover:bg-white/20"
                      }`}
                    >
                      {cat.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </section>

          {/* VIDEO GRID */}
          <section className="padding-x py-8">
            <div className="max-w-6xl mx-auto">
              <AnimatePresence mode="wait">
                {filteredVideos.length > 0 ? (
                  <motion.div
                    key={activeCategory}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.3 }}
                    className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                  >
                    {filteredVideos.map((video, index) => (
                      <motion.div
                        key={video.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.4, delay: index * 0.1 }}
                      >
                        <Link
                          href={video.videoUrl}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="block group"
                        >
                          <div className="relative rounded-2xl overflow-hidden bg-white/5 border border-white/10 hover:border-[#00aa55]/50 transition-all duration-300">
                            {/* Thumbnail Placeholder */}
                            <div className="aspect-video bg-gradient-to-br from-[#00aa55]/20 to-[#ff2f55]/20 relative group-hover:scale-[1.02] transition-transform duration-300">
                              <div className="absolute inset-0 flex items-center justify-center">
                                <div className="w-16 h-16 rounded-full bg-[#00aa55]/90 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                                  <Play size={24} className="text-black ml-1" fill="black" />
                                </div>
                              </div>
                              {/* Duration Badge */}
                              <div className="absolute bottom-3 right-3 px-2 py-1 rounded bg-black/70 text-xs font-NeueMontreal">
                                {video.duration}
                              </div>
                            </div>

                            {/* Content */}
                            <div className="p-5">
                              <div className="flex items-center gap-2 mb-2">
                                <span className="text-[10px] uppercase tracking-wider text-[#00aa55] bg-[#00aa55]/10 px-2 py-1 rounded">
                                  {categories.find(c => c.id === video.category)?.label}
                                </span>
                                <span className="text-xs text-white/50">
                                  {video.date}
                                </span>
                              </div>
                              <h3 className="font-neue-montreal text-lg font-medium group-hover:text-[#00aa55] transition-colors">
                                {video.title}
                              </h3>
                              <p className="font-NeueMontreal text-white/60 text-sm mt-2 line-clamp-2">
                                {video.description}
                              </p>
                            </div>
                          </div>
                        </Link>
                      </motion.div>
                    ))}
                  </motion.div>
                ) : (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="text-center py-16"
                  >
                    <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-white/10 flex items-center justify-center">
                      <Play size={32} className="text-white/50" />
                    </div>
                    <h3 className="font-neue-montreal text-xl mb-3">
                      No videos in this category yet
                    </h3>
                    <p className="font-NeueMontreal text-white/60 mb-6">
                      Request a topic and help us create the content you need!
                    </p>
                    <Link
                      href="#cta-strip"
                      className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#00aa55] text-black rounded-full font-NeueMontreal text-sm uppercase tracking-wider hover:bg-[#00cc66] transition-colors"
                    >
                      Request a Topic <ArrowRight size={14} />
                    </Link>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </section>

          {/* CTA STRIP - Per BNSCLIENT1.md */}
          <section id="cta-strip" className="padding-x py-16">
            <div className="max-w-4xl mx-auto">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6 }}
                className="text-center mb-10"
              >
                <span className="text-xs uppercase tracking-[0.2em] text-white/50">
                  Get Involved
                </span>
                <h2 className="font-neue-montreal text-2xl lg:text-3xl font-semibold mt-3">
                  Want to see a specific topic covered?
                </h2>
              </motion.div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Request a Topic */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: 0.1 }}
                  className="rounded-2xl bg-gradient-to-br from-[#00aa55]/20 via-white/5 to-[#00aa55]/10 border border-[#00aa55]/30 p-8 text-center hover:border-[#00aa55]/50 transition-colors"
                >
                  <div className="w-14 h-14 mx-auto mb-4 rounded-full bg-[#00aa55]/20 flex items-center justify-center">
                    <Plus size={24} className="text-[#00aa55]" />
                  </div>
                  <h3 className="font-neue-montreal text-xl font-medium mb-3">
                    Request a Topic
                  </h3>
                  <p className="font-NeueMontreal text-white/70 mb-6">
                    Suggest a budget topic you'd like us to explain in a video.
                  </p>
                  <Link
                    href="/contact"
                    className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#00aa55] text-black rounded-full font-NeueMontreal text-sm uppercase tracking-wider hover:bg-[#00cc66] transition-colors"
                  >
                    Submit Request <ArrowRight size={14} />
                  </Link>
                </motion.div>

                {/* Join Training */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                  className="rounded-2xl bg-gradient-to-br from-white/10 via-white/5 to-white/10 border border-white/20 p-8 text-center hover:border-white/30 transition-colors"
                >
                  <div className="w-14 h-14 mx-auto mb-4 rounded-full bg-white/10 flex items-center justify-center">
                    <Users size={24} className="text-white" />
                  </div>
                  <h3 className="font-neue-montreal text-xl font-medium mb-3">
                    Join Training
                  </h3>
                  <p className="font-NeueMontreal text-white/70 mb-6">
                    Learn how to analyze budgets and create your own stories.
                  </p>
                  <Link
                    href="/learn"
                    className="inline-flex items-center gap-2 px-5 py-2.5 bg-white text-black rounded-full font-NeueMontreal text-sm uppercase tracking-wider hover:bg-white/90 transition-colors"
                  >
                    Start Learning <ArrowRight size={14} />
                  </Link>
                </motion.div>
              </div>
            </div>
          </section>
        </main>

        {/* Footer */}
        <MainFooter />
      </div>
    </>
  );
}
