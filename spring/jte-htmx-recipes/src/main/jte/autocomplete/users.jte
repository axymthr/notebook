@import java.util.List

@param List<String> users

@if(users != null)
    <div id="userSuggestions" class="absolute bg-white shadow-md w-full mt-1 rounded-md z-10">
        @if(users.isEmpty())
            <div class="px-4 py-2 text-gray-500">No users found</div>
        @else
            <ul>
                @for(String user : users)
                    <li class="px-4 py-2 hover:bg-gray-100 cursor-pointer">${user}</li>
                @endfor
            </ul>
        @endif
    </div>
@endif