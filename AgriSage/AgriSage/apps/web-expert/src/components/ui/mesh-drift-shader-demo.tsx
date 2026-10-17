"use client"

import { ShaderBackground } from "@/components/ui/mesh-drift-shader";

export default function ShaderBackgroundDemo() {
  return (
    <div className="relative h-screen w-full overflow-hidden">
      <ShaderBackground className="h-full w-full" />
    </div>
  );
}
