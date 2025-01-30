@param com.example.jte.User user

<div class="cursor-pointer w-full border-gray-100 rounded-t border-b hover:bg-teal-100">
  <div class="flex w-full items-center p-2 pl-2 border-transparent border-l-2 relative hover:border-teal-100">
    <div class="w-6 flex flex-col items-center">
      <div class="flex relative w-6 h-6 bg-orange-500 justify-center items-center m-1 mr-2 rounded-full">
        <img class="rounded-full" alt="A" src="${user.avatar()}" />
      </div>
    </div>
    <div class="w-full items-center flex">
      <div class="mx-2 -mt-1">
        ${user.name()}
        <div class="text-xs truncate w-full normal-case font-normal -mt-1 text-gray-500">
          ${user.email()}
        </div>
      </div>
    </div>
  </div>
</div>