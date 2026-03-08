"use client";
import { Mail, MapPin, Phone } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";
import Newsletter from "./Newsletter";

const contactInfo = [
  {
    icon: <Mail size={20} strokeWidth={1.5} />,
    label: "Email",
    value: "info@budgetndiostory.org",
    href: "mailto:info@budgetndiostory.org",
  },
  {
    icon: <Phone size={20} strokeWidth={1.5} />,
    label: "Phone",
    value: "+254711106814",
    href: "tel:+254711106814",
  },
  {
    icon: <MapPin size={20} strokeWidth={1.5} />,
    label: "Location",
    value: "Nairobi, Kenya",
    href: "#",
  },
];

const socialLinks = [
  { name: "Facebook", href: "https://www.facebook.com/profile.php?id=61586898487932" },
  { name: "TikTok", href: "https://www.tiktok.com/@budget.ndio.story" },
  { name: "Instagram", href: "https://www.instagram.com/budgetndiostory" },
  { name: "X", href: "https://x.com/BudgetNdioStory" },
  { name: "YouTube", href: "https://www.youtube.com/@BudgetNdioStory" },
];

export default function MainFooter() {
  const [year, setYear] = useState(2026);

  useEffect(() => {
    setYear(new Date().getFullYear());
  }, []);

  return (
    <footer
      role="contentinfo"
      aria-label="Site footer"
      className="bg-[#0a0a0a] py-16 border-t border-white/10"
    >
      <div className="max-w-6xl mx-auto px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
          {/* Contact Info */}
          <div>
            <h3 className="font-neue-montreal text-lg font-medium text-white uppercase mb-6">
              Contact Info
            </h3>
            <div className="flex flex-col gap-4">
              {contactInfo.map((item, index) => (
                <div key={index} className="flex items-start gap-3">
                  <div className="text-white/60 mt-0.5">{item.icon}</div>
                  <div>
                    <p className="text-xs font-NeueMontreal text-white/50 mb-0.5">
                      {item.label}
                    </p>
                    <Link
                      href={item.href}
                      className="text-sm font-NeueMontreal text-white/80 hover:text-white transition-colors"
                    >
                      {item.value}
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Social Links */}
          <div>
            <h3 className="font-neue-montreal text-lg font-medium text-white uppercase mb-6">
              Follow Us
            </h3>
            <div className="flex flex-wrap gap-4">
              {socialLinks.map((social, index) => (
                <Link
                  key={index}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm font-NeueMontreal text-white/60 hover:text-white transition-colors"
                >
                  {social.name}
                </Link>
              ))}
            </div>
          </div>

          {/* Newsletter */}
          <div>
            <h3 className="font-neue-montreal text-lg font-medium text-white uppercase mb-6">
              Stay Updated
            </h3>
            <p className="text-sm font-NeueMontreal text-white/60 mb-4">
              Subscribe to our newsletter for budget insights and updates.
            </p>
            <Newsletter
              variant="dark"
              placeholder="Your email"
              buttonText="Subscribe"
            />
          </div>
        </div>

        {/* Bottom Bar - Tagline + Copyright + Legal Links */}
        <div className="mt-16 pt-10 border-t border-white/10">
          <div className="flex flex-col md:flex-row justify-between items-center gap-8 text-center md:text-left">
            {/* Tagline */}
            <p className="font-NeueMontreal text-white/70 text-lg md:text-xl font-light max-w-md">
              Follow The Budget. Find The Sory
            </p>

            {/* Copyright + Legal Links */}
            <div className="flex flex-col sm:flex-row items-center gap-6">
              <p className="text-sm font-NeueMontreal text-white/50">
                © {year} Budget Ndio Story. All rights reserved.
              </p>

              <div className="flex gap-6">
                <Link
                  href="/privacy"
                  className="text-sm font-NeueMontreal text-white/60 hover:text-white transition-colors"
                >
                  Privacy Policy
                </Link>
                <Link
                  href="/terms"
                  className="text-sm font-NeueMontreal text-white/60 hover:text-white transition-colors"
                >
                  Terms of Service
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}