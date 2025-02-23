//mobile button to toggle the mobile menu

   // Mobile Menu
   const menuButton = document.getElementById('menuButton');
   const mobileMenu = document.getElementById('mobileMenu');
   const notificationButton = document.getElementById('notificationButton');
   const notificationMenu = document.getElementById('notificationMenu');

   // Toggle the mobile menu when the menu button is clicked
   menuButton.addEventListener('click', (event) => {
       event.stopPropagation(); // Prevent click event from bubbling up to document
       
       // Close the notification dropdown if it's open when the menu button is clicked
       notificationMenu.classList.add('hidden');
       
       mobileMenu.classList.toggle('hidden');
       
       // Change the menu button icon based on menu visibility
       if (mobileMenu.classList.contains('hidden')) {
           menuButton.innerHTML = '<i class="fas fa-bars fa-lg"></i>'; // Hamburger icon
       } else {
           menuButton.innerHTML = '<i class="fas fa-times fa-lg"></i>'; // Close icon
       }
   });

   // Close the mobile menu if the user clicks outside of it
   document.addEventListener('click', (event) => {
       if (!mobileMenu.contains(event.target) && !menuButton.contains(event.target)) {
           mobileMenu.classList.add('hidden');
           menuButton.innerHTML = '<i class="fas fa-bars fa-lg"></i>'; // Reset button icon to hamburger
       }
   });

   // Prevent clicks inside the mobile menu from closing it
   mobileMenu.addEventListener('click', (event) => {
       event.stopPropagation(); // Prevent clicks inside the menu from triggering the document click event
   });
