<!DOCTYPE html>
<html lang="en">
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/1.4.6/tailwind.min.css" />
    <script src="https://unpkg.com/htmx.org@0.0.8"></script>
  </head>
  <body>
    <div class="">
      <div class="flex flex-col items-center">
        <div class="w-full md:w-1/2 flex flex-col items-center h-64">
          <div class="w-full px-4">
            <div class="flex flex-col items-center relative">
              <div class="w-full">
                <div class="my-2 p-1 bg-white flex border border-gray-200 rounded">
                  <div class="flex flex-auto flex-wrap"></div>
                  <input
                    name="q"
                    placeholder="Search by position"
                    class="p-1 px-2 appearance-none outline-none w-full text-gray-800"
                    hx-post="/q"
                    hx-trigger="keyup changed delay:500ms"
                    hx-target="#results"
                  />
                  <div class="text-gray-300 w-8 py-1 pl-2 pr-1 border-l flex items-center border-gray-200">
                    <button class="cursor-pointer w-6 h-6 text-gray-600 outline-none focus:outline-none">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="100%"
                        height="100%"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="feather feather-chevron-up w-4 h-4"
                      >
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
              <div class="htmx-indicator">Working</div>
              <div id="results" class="">
                @template("results", { "users": users })
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>