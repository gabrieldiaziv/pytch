"use client";

import {useDropzone} from 'react-dropzone'
import { useCallback } from 'react'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

function MyDropzone() {
  const onDrop = useCallback(acceptedFiles => {
    // Do something with the files
  }, [])
  const {getRootProps, getInputProps, isDragActive} = useDropzone({onDrop})

  return (
    <div className="text-black text-center p-16 bg-gray-100 border rounded-md border-neutral-200" {...getRootProps()}>

    {/* For menu bar later ?? */}
    {/* <div className="self-end text-center w-4/5 p-16 mt-10 bg-gray-100 border rounded-md border-neutral-200" {...getRootProps()}>  */}

    <div className="flex justify-center">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="purple" className=" w-12 h-12">
        <path fillRule="evenodd" d="M10.5 3.75a6 6 0 00-5.98 6.496A5.25 5.25 0 006.75 20.25H18a4.5 4.5 0 002.206-8.423 3.75 3.75 0 00-4.133-4.303A6.001 6.001 0 0010.5 3.75zm2.03 5.47a.75.75 0 00-1.06 0l-3 3a.75.75 0 101.06 1.06l1.72-1.72v4.94a.75.75 0 001.5 0v-4.94l1.72 1.72a.75.75 0 101.06-1.06l-3-3z" clipRule="evenodd" />
        </svg>

    </div>
    
      <input {...getInputProps()} />
      <p className='text-[#800080]'>Dropzone</p>
      {
        isDragActive ?
          <p>Drop the files here ...</p> :
          <p>Click to add files or drop just about anything on the Board...</p>
      }
    </div>
  )
}

export default async function UploadPage() {
    let items = ["test", "test", "test", "test", "test", "test", "test", "test", "test", "test", "test", "test"];
    let itemList=[];
    items.forEach((item,index)=>{
        itemList.push( 
            <Card style={{backgroundImage: `url(${'./assets/newjeans.png'})`}} className="flex flex-none h-4/5 w-1/5 bg-gray-100">
                <CardContent className="p-2 self-end text-white">
                    {item}
                </CardContent>
            </Card>
        )
    })
  return (
    <div className="flex flex-col w-full h-[100svh]">
      <div className="flex w-full h-[10%]">

      </div>
      <div className="flex w-full h-[90%]">
        <div className="flex flex-col h-full w-full p-4 gap-6">
            <MyDropzone/>

          
    
          <div className="flex flex-wrap h-full gap-4">
                {itemList}
          </div>
        </div>
      </div>
    </div>
  );
}