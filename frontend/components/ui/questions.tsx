import Image from 'next/image';

import {
  Item,
  ItemContent,
  ItemDescription,
  ItemGroup,
  ItemHeader,
  ItemTitle,
} from '@/components/ui/item';

export function Questions() {
  return (
    <div className='flex w-full max-w-xl flex-col gap-6'>
      <ItemGroup className='grid grid-cols-3 gap-4'>
        {models.map((model) => (
          <Item key={model.name} variant='outline'>
            <ItemHeader>
              <Image
                src={model.image}
                alt={model.name}
                width={128}
                height={128}
                className='aspect-square w-full rounded-sm object-cover'
              />
            </ItemHeader>
            <ItemContent>
              <ItemTitle>{model.name}</ItemTitle>
              <ItemDescription>{model.description}</ItemDescription>
            </ItemContent>
          </Item>
        ))}
      </ItemGroup>
    </div>
  );
}
