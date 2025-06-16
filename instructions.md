Start from the same file of objects I gave you.

Find the two objects (from all possible pairs) that are closest together, as determined by the smallest value of the “Delta R Squared” measure:
This is defined as the squared pseudo rapidity difference plus the squared azimuthal angle difference: **(eta_B - eta_A)^2 + (phi_B - phi_A)^2** 
If this value is greater than 0.4^2 = 0.16, then the algorithm halts and outputs the results (as summarized below).
If this value is less than or equal to the limit, then merge the two objects into a single object.
To merge objects, add their four-vectors: (E_A + E_B, pxA + pxB, pyA + pyB, pzA + pzB), and establish the collider coordinates (eta, phi, pt, mass) for the merged object.
Then, add it to the list of objects while removing the two original objects from which it is formed.  The list now has one fewer object in total.
Continue this process in a loop, finding the next pair of closest objects from the updated list.
Once you are done, (there are no remaining objects with Delta-R-Square <= 0.4^2), report how many “clustered jets” were identified, and what the collider coordinates of each of these objects is.

1. find the two closest objects determined by smallest Delta-R squared value **(eta_B - eta_A)^2 + (phi_B - phi_A)^2** 
2. if value of delta R squared is > to 0.16 then output it as a result
3. if it is <= then merge the objects, add the merged object back to the list and remove the pair from merging
4. merge using four vector components then make collider coordinates for the objects (why work in 4-vectors???)

Next Steps
----------
1) make a function to convert four vectors back to collider coordinates
2) work on merge or finish if else statements
3) re-check to make sure I am not double counting or leaving out mergers
  1. once finished all the mergers, recheck them against new items

