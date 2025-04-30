document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.dropdown > a').forEach(trigger => {
      trigger.addEventListener('click', function(e) {
        e.preventDefault();
        const parent = this.parentElement;
        parent.classList.toggle('active');
  
        // Close other dropdowns
        document.querySelectorAll('.dropdown').forEach(drop => {
          if (drop !== parent) drop.classList.remove('active');
        });
      });
    });
  
    // Close dropdown if clicked outside
    document.addEventListener('click', function(e) {
      if (!e.target.closest('.dropdown')) {
        document.querySelectorAll('.dropdown').forEach(drop => drop.classList.remove('active'));
      }
    });
  });