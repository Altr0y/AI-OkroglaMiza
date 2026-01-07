import Image from "next/image";

export default function GearButton() {
  return (
    <button className="relative w-10 h-10">
      {/* Light mode */}
      <Image
        src="/GearLightMode.png"
        alt="Settings"
        fill
        className="object-contain dark:hidden"
        priority
      />

      {/* Dark mode */}
      <Image
        src="/GearDarkMode.png"
        alt="Settings"
        fill
        className="object-contain hidden dark:block"
        priority
      />
    </button>
  );
}
