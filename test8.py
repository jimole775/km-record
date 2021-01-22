from h5py import Dataset, Group, File
with File('12306.image.model.h5','r') as f:
  # for fkey in f.keys():
  #   print(f[fkey], fkey)
  next_group = f["model_weights"] # 从上面的结果可以发现根目录/下有个dogs的group,所以我们来研究一下它
  for fkey in next_group.keys():
    print(next_group[fkey], next_group[fkey].name)
    # if isinstance(next_group[fkey], Dataset):