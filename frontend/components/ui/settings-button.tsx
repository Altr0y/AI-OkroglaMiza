import Image from "next/image";


import { Button } from '@/components/ui/button';

export default function GearButton() {
  return (
    <Button variant="outline" size="icon">
      <div className="relative w-5 h-5">
        {/* light */}
        <Image
          src="/gear.png"
          alt="Settings"
          fill
          className="object-contain dark:hidden"
        />
        {/* dark */}
        <Image
          src="/gear2.png"
          alt="Settings"
          fill
          className="object-contain hidden dark:block"
        />
      </div>
    </Button>
  );
}

