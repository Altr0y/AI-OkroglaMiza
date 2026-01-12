'use client'

import Image from "next/image"
import { Button } from '@/components/ui/button'
import { useState } from "react"
import { useTranslations } from 'next-intl'

export default function SettingsButton() {
  const [open, setOpen] = useState(false)
  const [settingsOptions, setSettings] = useState(0)

  const t = useTranslations('SettingsPage_dataControl')
  const a = useTranslations('SettingPage_notificationSet')
  const c = useTranslations('SettingPage_security')

  return (
    <>
      <Button variant="outline" size="icon" onClick={() => setOpen(true)}>
        <div className="relative w-5 h-5">
          <Image
            src="/gearLight.png"
            alt="Settings"
            fill
            className="object-contain dark:hidden"
          />
          <Image
            src="/gearDark.png"
            alt="Settings"
            fill
            className="object-contain hidden dark:block"
          />
        </div>
      </Button>

      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="w-[32rem] rounded-lg bg-white dark:bg-black p-0 flex">

            <div className="w-[30%] p-4 border-r dark:border-white/10">
              <Button className="mt-4 w-30" onClick={() => setSettings(0)}>General</Button>
              <Button className="mt-4 w-30" onClick={() => setSettings(1)}>Notifications</Button>
              <Button className="mt-4 w-30" onClick={() => setSettings(2)}>Security</Button>
              <Button className="mt-4" onClick={() => setOpen(false)}>Zapri</Button>
            </div>

            <div className="w-[70%] p-4">
              {settingsOptions === 0 && (
                <div>
                  <h1>{t('dataControlSet')}</h1>

                  <div className="flex items-center justify-between mt-2">
                    <span>{t('sharedLinks')}</span>
                    <input type="checkbox" className="form-checkbox" />
                  </div>
                  <div className="flex items-center justify-between mt-2">
                    <span>{t('archivedChats')}</span>
                    <input type="checkbox" className="form-checkbox" />
                  </div>
                  <div className="flex items-center justify-between mt-2">
                    <span>{t('archiveAllChats')}</span>
                    <input type="checkbox" className="form-checkbox" />
                  </div>
                  <div className="flex items-center justify-between mt-2">
                    <span>{t('deleateAllChats')}</span>
                    <input type="checkbox" className="form-checkbox" />
                  </div>
                </div>
              )}

              {settingsOptions === 1 && (
                <div>
                  <h1>{a('notificationSet')}</h1>

                  <div className="flex items-center justify-between mt-2">
                    <span>{a('getNotifiedRes')}</span>
                    <input type="checkbox" className="form-checkbox" />
                  </div>
                  <div className="flex items-center justify-between mt-2">
                    <span>{a('getNotifiedGroup')}</span>
                    <input type="checkbox" className="form-checkbox" />
                  </div>
                  <div className="flex items-center justify-between mt-2">
                    <span>{a('getNotifiedTask')}</span>
                    <input type="checkbox" className="form-checkbox" />
                  </div>
                </div>
              )}

              {settingsOptions === 2 && (
                <div>
                  <h1>{c('securitySet')}</h1>

                  <div className="flex items-center justify-between mt-2">
                    <span>{c('multyFactor')}</span>
                    <input type="checkbox" className="form-checkbox" />
                  </div>
                  <div className="flex items-center justify-between mt-2">
                    <span>{c('logOut')}</span>
                    <input type="checkbox" className="form-checkbox" />
                  </div>
                  <div className="flex items-center justify-between mt-2">
                    <span>{c('logOutAll')}</span>
                    <input type="checkbox" className="form-checkbox" />
                  </div>
                </div>
              )}
            </div>

          </div>
        </div>
      )}
    </>
  )
}
