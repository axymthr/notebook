@import java.util.List
@import com.example.jte.User
@param List<User> users

<div id="results" class="">
  <div class="shadow bg-white top-100 z-40 w-full lef-0 rounded max-h-select overflow-y-auto">
    <div class="flex flex-col w-full">
      @for(User user : users)
        @template("user", user)
      @endfor
    </div>
  </div>
</div>