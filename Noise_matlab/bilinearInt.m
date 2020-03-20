function s = bilinearInt( M, coord )

lower_indices = zeros(2,1);
upper_indices = zeros(2,1);

for i=1:2

  if mod(coord(i),1) > 0
    lower_indices(i) = floor(coord(i));
    upper_indices(i) = lower_indices(i)+1;
  else
    upper_indices(i) = ceil(coord(i));
    lower_indices(i) = upper_indices(i)-1;
  end
      
end

 
A = (upper_indices(1)-coord(1)) / (upper_indices(1)-lower_indices(1)) * lookup(M,[lower_indices(2);lower_indices(1)]) + (coord(1)-lower_indices(1)) / (upper_indices(1)-lower_indices(1)) * lookup(M,[lower_indices(2);upper_indices(1)]);
B = (upper_indices(1)-coord(1)) / (upper_indices(1)-lower_indices(1)) * lookup(M,[upper_indices(2);lower_indices(1)]) + (coord(1)-lower_indices(1)) / (upper_indices(1)-lower_indices(1)) * lookup(M,[upper_indices(2);upper_indices(1)]);
s = (upper_indices(2)-coord(2)) / (upper_indices(2)-lower_indices(2)) * A + (coord(2)-lower_indices(2)) / (upper_indices(2)-lower_indices(2)) * B;

end

function v = lookup(M,indices)

  indices_rectified = max([1;1],indices+[1;1]);
  indices_rectified2 = min( [size(M,1);size(M,2)],indices_rectified );
  v = M(indices_rectified2(1),indices_rectified2(2));
end