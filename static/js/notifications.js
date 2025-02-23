//notification button to toggle the dropdown visibility on click (for mobile & desktop)

   // Toggle the notification dropdown when the notification button is clicked
   notificationButton.addEventListener('click', function(event) {
       event.preventDefault(); // Prevent page refresh or other actions
       const dropdown = notificationMenu;
       dropdown.classList.toggle('hidden');
   });

   // Close dropdown when clicking outside of the dropdown area
   window.addEventListener('click', function(event) {
       const dropdown = notificationMenu;
       const notificationIcon = notificationButton;
       
       // Close the dropdown if the click is outside the notification icon or dropdown
       if (!notificationIcon.contains(event.target) && !dropdown.contains(event.target)) {
           dropdown.classList.add('hidden');
       }
   });
