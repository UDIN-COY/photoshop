import React, { useState } from 'react';
import { SlidersHorizontal } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';

export type ToolCategory = 'adjust' | 'geometry' | 'color' | 'filters' | 'restore' | 'segment' | null;

interface SidebarProps {
  activeCategory: ToolCategory;
  onApplyTool: (endpoint: string, params?: Record<string, string | number>) => void;
  isProcessing: boolean;
  disabled: boolean;
}

export default function Sidebar({ activeCategory, onApplyTool, isProcessing, disabled }: SidebarProps) {
  // Enhancement
  const [brightness, setBrightness] = useState(0);
  const [contrast, setContrast] = useState(0);
  const [smoothType, setSmoothType] = useState('gaussian');
  
  // Geometry
  const [rotateAngle, setRotateAngle] = useState(0);
  const [flipMode, setFlipMode] = useState('1'); 
  const [resizeScale, setResizeScale] = useState(1.0);
  const [crop, setCrop] = useState({ x1: 0, y1: 0, x2: 100, y2: 100 });
  const [translate, setTranslate] = useState({ tx: 0, ty: 0 });

  // Filter & Edge
  const [threshVal, setThreshVal] = useState(127);
  const [edgeType, setEdgeType] = useState('canny');
  const [morphType, setMorphType] = useState('erosion');
  const [kernelSize, setKernelSize] = useState(5);

  // Color
  const [hue, setHue] = useState(0);
  const [sat, setSat] = useState(0);
  const [splitChannel, setSplitChannel] = useState('0');

  // Segmentation
  const [kMeansValue, setKMeansValue] = useState(4);

  const handleApply = (endpoint: string, params: Record<string, string|number> = {}) => {
    if (disabled || isProcessing) return;
    onApplyTool(endpoint, params);
  }

  if (!activeCategory) {
    return (
      <div className="w-[300px] flex-shrink-0 border-l bg-card flex flex-col h-full shadow-sm z-10 p-6 items-center justify-center text-center text-muted-foreground">
        <div className="w-12 h-12 rounded-full bg-muted flex items-center justify-center mb-4">
          <SlidersHorizontal className="w-5 h-5 opacity-50" />
        </div>
        <p className="text-sm font-medium text-foreground mb-1">Siap Beraksi</p>
        <p className="text-xs">Pilih alat dari panel kiri untuk melihat propertinya.</p>
      </div>
    );
  }

  let title = '';
  let description = '';
  if (activeCategory === 'adjust') { title = 'Penyesuaian'; description = 'Kecerahan, kontras & buram'; }
  if (activeCategory === 'geometry') { title = 'Geometri'; description = 'Transformasi dan ukuran gambar'; }
  if (activeCategory === 'color') { title = 'Warna'; description = 'Kanal dan pengaturan rona'; }
  if (activeCategory === 'filters') { title = 'Filter'; description = 'Tepi dan morfologi'; }
  if (activeCategory === 'restore') { title = 'Pemulihan'; description = 'Penghilang derau dan perbaikan'; }
  if (activeCategory === 'segment') { title = 'Segmentasi'; description = 'Klasterisasi dan deteksi (ML)'; }

  return (
    <div className="w-[300px] flex-shrink-0 border-l bg-card flex flex-col h-full shadow-sm z-10">
      <div className="p-4 border-b bg-background sticky top-0 z-20 h-14 flex items-center">
        <div>
          <h2 className="font-semibold text-sm tracking-wide text-foreground uppercase mt-1.5">{title}</h2>
          <p className="text-xs text-muted-foreground mt-0.5">{description}</p>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto">
        <div className="p-3 space-y-4">
          
          {activeCategory === 'adjust' && (
            <>
              <div className="space-y-4 bg-muted/30 p-4 rounded-xl border border-border/50">
                <div className="flex justify-between items-center text-xs">
                  <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Kecerahan</Label>
                  <span className="font-mono text-muted-foreground">{brightness}</span>
                </div>
                <Slider min={-100} max={100} step={1} value={[brightness]} onValueChange={(v) => setBrightness(v[0])} disabled={disabled} />
                
                <div className="flex justify-between items-center text-xs mt-4">
                  <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Kontras</Label>
                  <span className="font-mono text-muted-foreground">{contrast}</span>
                </div>
                <Slider min={-100} max={100} step={1} value={[contrast]} onValueChange={(v) => setContrast(v[0])} disabled={disabled} />
                
                <Button variant="default" size="sm" className="w-full mt-2" onClick={() => handleApply('/api/enhance/brightness-contrast', { brightness, contrast })}>
                  Terapkan Pengaturan
                </Button>
              </div>

              <div className="grid grid-cols-2 gap-2 bg-muted/30 p-4 rounded-xl border border-border/50">
                <Button variant="outline" size="sm" onClick={() => handleApply('/api/enhance/equalize')}>Ekualisasi Hist</Button>
                <Button variant="outline" size="sm" onClick={() => handleApply('/api/enhance/sharpen')}>Pertajam</Button>
              </div>

              <div className="space-y-4 bg-muted/30 p-4 rounded-xl border border-border/50">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Pengeburaman</Label>
                <Select value={smoothType} onValueChange={setSmoothType} disabled={disabled}>
                  <SelectTrigger className="h-8 text-xs"><SelectValue placeholder="Algoritma" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="gaussian">Buram Gaussian</SelectItem>
                    <SelectItem value="average">Buram Rata-rata</SelectItem>
                    <SelectItem value="median">Buram Median</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/enhance/smooth', { ftype: smoothType })}>Terapkan Buram</Button>
              </div>
            </>
          )}

          {activeCategory === 'geometry' && (
            <>
              <div className="space-y-4">
                <div className="flex justify-between items-center text-xs">
                  <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Rotasi</Label>
                  <span className="font-mono text-muted-foreground">{rotateAngle}°</span>
                </div>
                <Slider min={-180} max={180} step={1} value={[rotateAngle]} onValueChange={(v) => setRotateAngle(v[0])} disabled={disabled} />
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/geom/rotate', { angle: rotateAngle })}>Putar</Button>
              </div>

              <Separator />

              <div className="space-y-4">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Balikan Gambar</Label>
                <Select value={flipMode} onValueChange={setFlipMode} disabled={disabled}>
                  <SelectTrigger className="h-8 text-xs"><SelectValue placeholder="Mode" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1">Horizontal (Sumbu-Y)</SelectItem>
                    <SelectItem value="0">Vertikal (Sumbu-X)</SelectItem>
                    <SelectItem value="-1">Kedua Sumbu</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/geom/flip', { mode: parseInt(flipMode) })}>Balik</Button>
              </div>

              <Separator />

              <div className="space-y-4">
                <div className="flex justify-between items-center text-xs">
                  <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Skala</Label>
                  <span className="font-mono text-muted-foreground">{resizeScale.toFixed(2)}x</span>
                </div>
                <Slider min={0.1} max={3.0} step={0.1} value={[resizeScale]} onValueChange={(v) => setResizeScale(v[0])} disabled={disabled} />
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/geom/resize', { scale: resizeScale })}>Ubah Skala</Button>
              </div>

              <Separator />

              <div className="space-y-4">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Pergeseran</Label>
                <div className="grid grid-cols-2 gap-2">
                  <Input className="h-8 text-xs font-mono" type="number" placeholder="X" value={translate.tx} onChange={e => setTranslate({...translate, tx: +e.target.value})} disabled={disabled} />
                  <Input className="h-8 text-xs font-mono" type="number" placeholder="Y" value={translate.ty} onChange={e => setTranslate({...translate, ty: +e.target.value})} disabled={disabled} />
                </div>
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/geom/translate', translate)}>Geser</Button>
              </div>

              <Separator />

              <div className="space-y-4">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Area Potong</Label>
                <div className="grid grid-cols-2 gap-2">
                  <Input className="h-8 text-xs font-mono" type="number" placeholder="X1" value={crop.x1} onChange={e => setCrop({...crop, x1: +e.target.value})} disabled={disabled} />
                  <Input className="h-8 text-xs font-mono" type="number" placeholder="Y1" value={crop.y1} onChange={e => setCrop({...crop, y1: +e.target.value})} disabled={disabled} />
                  <Input className="h-8 text-xs font-mono" type="number" placeholder="X2" value={crop.x2} onChange={e => setCrop({...crop, x2: +e.target.value})} disabled={disabled} />
                  <Input className="h-8 text-xs font-mono" type="number" placeholder="Y2" value={crop.y2} onChange={e => setCrop({...crop, y2: +e.target.value})} disabled={disabled} />
                </div>
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/geom/crop', crop)}>Potong</Button>
              </div>
            </>
          )}

          {activeCategory === 'restore' && (
            <>
              <div className="space-y-3">
                <Button variant="outline" size="sm" className="w-full justify-start font-normal" onClick={() => handleApply('/api/restore/gaussian')}>
                  Hapus Derau Gaussian
                </Button>
                <Button variant="outline" size="sm" className="w-full justify-start font-normal" onClick={() => handleApply('/api/restore/median')}>
                  Hapus Derau Median (S&P)
                </Button>
              </div>
            </>
          )}

          {activeCategory === 'color' && (
            <>
              <div className="bg-muted/30 p-4 rounded-xl border border-border/50">
                <Button variant="outline" size="sm" className="w-full" onClick={() => handleApply('/api/color/grayscale')}>Konversi ke Keabuan</Button>
              </div>

               <div className="space-y-4 bg-muted/30 p-4 rounded-xl border border-border/50">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Ekstrak Kanal</Label>
                <Select value={splitChannel} onValueChange={setSplitChannel} disabled={disabled}>
                  <SelectTrigger className="h-8 text-xs"><SelectValue placeholder="Kanal" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="2">Kanal Merah</SelectItem>
                    <SelectItem value="1">Kanal Hijau</SelectItem>
                    <SelectItem value="0">Kanal Biru</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/color/split-channel', { channel: parseInt(splitChannel) })}>Ekstrak</Button>
              </div>

              <Separator />

              <div className="space-y-4">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground block text-center">
                  Penyesuaian HSV
                </Label>
                <div className="flex justify-between items-center text-xs mt-2">
                  <Label className="text-xs text-muted-foreground">Geser Rona (Hue)</Label>
                  <span className="font-mono text-muted-foreground">{hue}</span>
                </div>
                <Slider min={-180} max={180} step={1} value={[hue]} onValueChange={(v) => setHue(v[0])} disabled={disabled} />
                
                <div className="flex justify-between items-center text-xs mt-3">
                  <Label className="text-xs text-muted-foreground">Saturasi</Label>
                  <span className="font-mono text-muted-foreground">{sat}</span>
                </div>
                <Slider min={-255} max={255} step={1} value={[sat]} onValueChange={(v) => setSat(v[0])} disabled={disabled} />
                
                <Button variant="secondary" size="sm" className="w-full mt-2" onClick={() => handleApply('/api/color/hsv-adjust', { hue_shift: hue, sat_shift: sat })}>Terapkan HSV</Button>
              </div>
            </>
          )}

          {activeCategory === 'filters' && (
            <>
              <div className="space-y-4">
                <div className="flex justify-between items-center text-xs">
                  <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Batas Ambang (Threshold)</Label>
                  <span className="font-mono text-muted-foreground">{threshVal}</span>
                </div>
                <Slider min={0} max={255} step={1} value={[threshVal]} onValueChange={(v) => setThreshVal(v[0])} disabled={disabled} />
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/edge/threshold', { thresh_val: threshVal })}>Terapkan Threshold</Button>
              </div>

              <Separator />

              <div className="space-y-4">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Algoritma Tepi</Label>
                <Select value={edgeType} onValueChange={setEdgeType} disabled={disabled}>
                  <SelectTrigger className="h-8 text-xs"><SelectValue placeholder="Algoritma" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="canny">Canny</SelectItem>
                    <SelectItem value="sobel">Sobel</SelectItem>
                    <SelectItem value="prewitt">Prewitt</SelectItem>
                    <SelectItem value="robert">Robert</SelectItem>
                    <SelectItem value="laplacian">Laplacian</SelectItem>
                    <SelectItem value="log">Laplacian of Gaussian</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/edge/detect', { etype: edgeType })}>Deteksi Tepi</Button>
              </div>

              <Separator />

              <div className="space-y-4">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Morfologi</Label>
                <Select value={morphType} onValueChange={setMorphType} disabled={disabled}>
                  <SelectTrigger className="h-8 text-xs"><SelectValue placeholder="Operasi" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="erosion">Erosi (Erosion)</SelectItem>
                    <SelectItem value="dilation">Dilasi (Dilation)</SelectItem>
                    <SelectItem value="opening">Opening</SelectItem>
                    <SelectItem value="closing">Closing</SelectItem>
                  </SelectContent>
                </Select>
                
                <div className="flex justify-between items-center text-xs mt-3">
                  <Label className="text-xs text-muted-foreground">Ukuran Kernel</Label>
                  <span className="font-mono text-muted-foreground">{kernelSize}x{kernelSize}</span>
                </div>
                <Slider min={1} max={21} step={2} value={[kernelSize]} onValueChange={(v) => setKernelSize(v[0])} disabled={disabled} />
                
                <Button variant="secondary" size="sm" className="w-full mt-2" onClick={() => handleApply('/api/morphology', { mtype: morphType, kernel_size: kernelSize })}>Terapkan Morfologi</Button>
              </div>
            </>
          )}

          {activeCategory === 'segment' && (
            <>
              <div className="space-y-4">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Klasterisasi K-Means</Label>
                <div className="flex justify-between items-center text-xs mt-1">
                  <span className="text-xs text-muted-foreground">K (Jumlah Klaster)</span>
                  <span className="font-mono text-muted-foreground">{kMeansValue}</span>
                </div>
                <Slider min={2} max={16} step={1} value={[kMeansValue]} onValueChange={(v) => setKMeansValue(v[0])} disabled={disabled} />
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/segment/kmeans', { k: kMeansValue })}>Terapkan K-Means</Button>
              </div>

              <Separator />
              
              <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground block">Metode Lainnya</Label>
              <div className="space-y-2 mt-4">
                <Button variant="outline" size="sm" className="w-full justify-start font-normal" onClick={() => handleApply('/api/segment/edge-based')}>Tepi (Edge-Based)</Button>
                <Button variant="default" size="sm" className="w-full justify-start font-medium" onClick={() => handleApply('/api/ml/detect-objects')}>
                  Deteksi Objek CNN
                </Button>
              </div>
            </>
          )}

        </div>
      </div>
    </div>
  );
}

